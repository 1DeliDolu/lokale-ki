"""
ChatGPT benzeri sohbet botu için Gradio arayüzü
"""

import gradio as gr
from chatbot_module import ChatGPTLikeBot, ModelPresets, ConversationManager
from image_analysis import ImageAnalyzer
from typing import List, Tuple, Optional
import json
import os

# Global değişkenler
chatbot = None
conversation_manager = None
image_analyzer = None
current_conversation_id = None

def initialize_chatbot():
    """
    Sohbet botunu başlat
    """
    global chatbot
    if chatbot is None:
        config = ModelPresets.conversational_model()
        chatbot = ChatGPTLikeBot(config)
    return chatbot

def initialize_conversation_manager():
    """
    Konuşma yöneticisini başlat
    """
    global conversation_manager
    if conversation_manager is None:
        conversation_manager = ConversationManager()
        # Varsayılan botları oluştur
        conversation_manager.create_bot("assistant", ModelPresets.helpful_assistant())
        conversation_manager.create_bot("creative", ModelPresets.creative_writer())
        conversation_manager.create_bot("technical", ModelPresets.technical_expert())
    return conversation_manager

def initialize_image_analyzer():
    """
    Görsel analiz botunu başlat
    """
    global image_analyzer
    if image_analyzer is None:
        from image_analysis import ImageAnalyzer
        image_analyzer = ImageAnalyzer()
    return image_analyzer

def chat_with_bot(message: str, chat_history: List[Tuple[str, str]], bot_type: str = "assistant") -> Tuple[List[Tuple[str, str]], str]:
    """
    Sohbet botu ile konuşma
    
    Args:
        message (str): Kullanıcı mesajı
        chat_history (List): Sohbet geçmişi
        bot_type (str): Bot türü
        
    Returns:
        Tuple: Güncellenmiş sohbet geçmişi ve boş input
    """
    try:
        if not message.strip():
            return chat_history, ""
        
        # Conversation manager'ı başlat
        manager = initialize_conversation_manager()
        
        # Bot ile sohbet et
        response = manager.chat_with_bot(bot_type, message)
        
        # Sohbet geçmişini güncelle
        chat_history.append((message, response))
        
        return chat_history, ""
        
    except Exception as e:
        error_response = f"Üzgünüm, bir hata oluştu: {str(e)}"
        chat_history.append((message, error_response))
        return chat_history, ""

def analyze_image_and_chat(image, message: str, chat_history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
    """
    Görsel analiz et ve sohbet et
    
    Args:
        image: Yüklenen görsel
        message (str): Kullanıcı mesajı
        chat_history (List): Sohbet geçmişi
        
    Returns:
        Tuple: Güncellenmiş sohbet geçmişi ve boş input
    """
    try:
        # Görsel analiz et
        if image is not None:
            img_analyzer = initialize_image_analyzer()
            result = img_analyzer.analyze_image(image)
            
            if result['success']:
                image_description = f"📸 Görsel Analizi:\n🏷️ Başlık: {result['title']}\n📝 Açıklama: {result['caption']}"
                
                # Eğer kullanıcı mesajı varsa, görsel ile birlikte sor
                if message.strip():
                    combined_message = f"{image_description}\n\nKullanıcı sorusu: {message}"
                else:
                    combined_message = f"{image_description}\n\nBu görsel hakkında ne düşünüyorsun?"
                
                # Chatbot ile konuş
                manager = initialize_conversation_manager()
                response = manager.chat_with_bot("assistant", combined_message)
                
                chat_history.append((f"📸 [Görsel yüklendi] {message}" if message else "📸 [Görsel yüklendi]", response))
            else:
                error_msg = "Görsel analiz edilemedi. Lütfen başka bir görsel deneyin."
                chat_history.append((f"📸 [Görsel yüklendi] {message}" if message else "📸 [Görsel yüklendi]", error_msg))
        else:
            # Sadece metin mesajı
            if message.strip():
                return chat_with_bot(message, chat_history)
        
        return chat_history, ""
        
    except Exception as e:
        error_response = f"Hata oluştu: {str(e)}"
        chat_history.append((f"📸 [Görsel] {message}" if message else "📸 [Görsel]", error_response))
        return chat_history, ""

def get_conversation_list() -> str:
    """
    Konuşma listesini getir
    
    Returns:
        str: Formatlanmış konuşma listesi
    """
    try:
        bot = initialize_chatbot()
        conversations = bot.get_conversation_list()
        
        if not conversations:
            return "Henüz konuşma yok."
        
        formatted_list = "📋 **Konuşma Geçmişi:**\n\n"
        for conv in conversations[:10]:  # Son 10 konuşma
            title = conv['title'][:50] + "..." if len(conv['title']) > 50 else conv['title']
            date = conv['created_at'][:19].replace('T', ' ')
            formatted_list += f"• **{title}**\n  📅 {date}\n\n"
        
        return formatted_list
        
    except Exception as e:
        return f"Konuşma listesi alınamadı: {str(e)}"

def clear_conversation() -> Tuple[List, str]:
    """
    Konuşmayı temizle
    
    Returns:
        Tuple: Boş sohbet geçmişi ve başlangıç mesajı
    """
    global current_conversation_id
    current_conversation_id = None
    
    bot = initialize_chatbot()
    bot.start_new_conversation()
    
    return [], "🆕 Yeni konuşma başlatıldı! Size nasıl yardımcı olabilirim?"

def create_chatbot_interface():
    """
    Sohbet botu Gradio arayüzünü oluştur
    """
    
    with gr.Blocks(title="🤖 ChatGPT Benzeri Sohbet Botu", theme=gr.themes.Soft()) as interface:
        
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>🤖 ChatGPT Benzeri Sohbet Botu</h1>
            <p>Açık kaynak LLM'ler ile yapay zeka sohbeti</p>
        </div>
        """)
        
        with gr.Tab("💬 Sohbet"):
            with gr.Row():
                with gr.Column(scale=3):                    # Ana sohbet arayüzü
                    chatbot_display = gr.Chatbot(
                        label="🤖 Sohbet",
                        height=500,
                        avatar_images=None
                    )
                    
                    with gr.Row():
                        msg_input = gr.Textbox(
                            label="💬 Mesajınız",
                            placeholder="Bir şeyler yazın...",
                            lines=2,
                            scale=4
                        )
                        send_btn = gr.Button("📤 Gönder", variant="primary", scale=1)
                    
                    with gr.Row():
                        clear_btn = gr.Button("🗑️ Temizle", variant="secondary")
                        history_btn = gr.Button("📋 Geçmiş", variant="secondary")
                
                with gr.Column(scale=1):
                    # Bot türü seçimi
                    bot_type = gr.Radio(
                        ["assistant", "creative", "technical"],
                        value="assistant",
                        label="🤖 Bot Türü",
                        info="Hangi tür asistan istersiniz?"
                    )
                    
                    # Sistem bilgileri
                    gr.HTML("""
                    <div style="padding: 15px; background: #f5f5f5; border-radius: 10px; margin-top: 20px;">
                        <h4>ℹ️ Bot Türleri</h4>
                        <p><b>🤝 Assistant:</b> Genel yardımcı asistan</p>
                        <p><b>🎨 Creative:</b> Yaratıcı yazım ve hikayeler</p>
                        <p><b>⚙️ Technical:</b> Programlama ve teknik konular</p>
                    </div>
                    """)
        
        with gr.Tab("📸 Görsel + Sohbet"):
            with gr.Row():
                with gr.Column(scale=2):
                    # Görsel yükleme
                    image_input = gr.Image(
                        type="numpy",
                        label="📸 Görsel Yükleyin"
                    )
                    
                    # Görsel ile ilgili soru
                    image_msg_input = gr.Textbox(
                        label="❓ Görsel hakkında soru (isteğe bağlı)",
                        placeholder="Bu görsel hakkında ne bilmek istiyorsunuz?",
                        lines=3
                    )
                    
                    analyze_btn = gr.Button("🔍 Analiz Et & Sor", variant="primary")
                
                with gr.Column(scale=2):                    # Görsel sohbet geçmişi
                    image_chatbot = gr.Chatbot(
                        label="📸 Görsel Sohbet",
                        height=400,
                        avatar_images=None
                    )
        
        with gr.Tab("📊 İstatistikler"):
            with gr.Column():
                gr.HTML("<h3>📈 Bot İstatistikleri</h3>")
                
                stats_display = gr.HTML()
                refresh_stats_btn = gr.Button("🔄 Yenile", variant="secondary")
                
                # Konuşma geçmişi
                conversation_history = gr.Textbox(
                    label="📋 Konuşma Geçmişi",
                    lines=15,
                    max_lines=20
                )
        
        # Event handlers
        
        # Ana sohbet
        send_btn.click(
            chat_with_bot,
            inputs=[msg_input, chatbot_display, bot_type],
            outputs=[chatbot_display, msg_input]
        )
        
        msg_input.submit(
            chat_with_bot,
            inputs=[msg_input, chatbot_display, bot_type],
            outputs=[chatbot_display, msg_input]
        )
        
        # Konuşma temizleme
        clear_btn.click(
            clear_conversation,
            outputs=[chatbot_display, msg_input]
        )
        
        # Konuşma geçmişi
        history_btn.click(
            get_conversation_list,
            outputs=conversation_history
        )
        
        # Görsel analiz
        analyze_btn.click(
            analyze_image_and_chat,
            inputs=[image_input, image_msg_input, image_chatbot],
            outputs=[image_chatbot, image_msg_input]
        )
        
        # İstatistik yenileme
        def update_stats():
            try:
                bot = initialize_chatbot()
                info = bot.get_model_info()
                
                stats_html = f"""
                <div style="padding: 15px; background: #f0f8ff; border-radius: 10px;">
                    <h4>🤖 Model Bilgileri</h4>
                    <p><b>Model:</b> {info['model_name']}</p>
                    <p><b>Device:</b> {info['device']}</p>
                    <p><b>CUDA:</b> {'✅ Mevcut' if info['cuda_available'] else '❌ Mevcut değil'}</p>
                </div>
                """
                return stats_html
            except Exception as e:
                return f"❌ İstatistik yüklenemedi: {str(e)}"
        
        refresh_stats_btn.click(
            update_stats,
            outputs=stats_display
        )
        
        # Sayfa yüklendiğinde istatistikleri göster
        interface.load(
            update_stats,
            outputs=stats_display
        )
    
    return interface

def launch_chatbot_app(
    server_name: str = "0.0.0.0",
    server_port: int = 7861,
    share: bool = False
):
    """
    Sohbet botu uygulamasını başlat
    
    Args:
        server_name (str): Sunucu adı
        server_port (int): Port numarası
        share (bool): Public link oluştur
    """
    print("🚀 ChatGPT Benzeri Sohbet Botu başlatılıyor...")
    
    interface = create_chatbot_interface()
    
    interface.launch(
        server_name=server_name,
        server_port=server_port,
        share=share,
        show_api=False
    )