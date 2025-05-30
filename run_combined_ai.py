"""
Birleşik AI Modülleri - Görsel Analiz + ChatGPT Benzeri Sohbet
Ana uygulama launcher'ı
"""

import gradio as gr
from gradio_interface import create_gradio_interface as create_image_interface
from chatbot_gradio_interface import create_chatbot_interface
import sys

def create_combined_interface():
    """
    Birleşik arayüz oluştur - Görsel Analiz + Sohbet Botu
    """
    
    # Ana tema
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
        neutral_hue="slate"
    )
    
    with gr.Blocks(title="🤖 AI Modülleri - Görsel Analiz & ChatGPT", theme=theme) as combined_interface:
        
        # Başlık
        gr.HTML("""
        <div style="text-align: center; padding: 30px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0; font-size: 2.5em;">🤖 AI Modülleri Hub</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em;">Görsel Analiz & ChatGPT Benzeri Sohbet Botu</p>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">Üretici Yapay Zeka ile Tam Donanımlı AI Asistanınız</p>
        </div>
        """)
        
        # Ana tab'lar
        with gr.Tab("📸 Görsel Analiz AI"):
            gr.HTML("""
            <div style="text-align: center; padding: 15px; background: #f0f8ff; border-radius: 10px; margin-bottom: 15px;">
                <h3>📸 AI Görsel Açıklayıcı</h3>
                <p>Fotoğraflarınızı yükleyin, AI otomatik olarak açıklasın!</p>
            </div>
            """)
            
            # Görsel analiz arayüzünü içe aktar
            try:
                from gradio_interface import (
                    process_image_gradio, 
                    save_analysis_gradio
                )
                
                with gr.Row():
                    with gr.Column(scale=2):
                        # Ana görsel analiz
                        image_input = gr.Image(type="numpy", label="📸 Görselinizi Yükleyin")
                        analyze_btn = gr.Button("🔍 Analiz Et", variant="primary", size="lg")
                        
                        # Sonuçlar
                        with gr.Row():
                            result_image = gr.Image(type="numpy", label="📷 Yüklenen Görsel")
                        
                        analysis_result = gr.Textbox(
                            label="🤖 AI Analiz Sonucu", 
                            lines=6,
                            placeholder="Analiz sonucu burada görünecek..."
                        )
                        
                        status_text = gr.Textbox(label="📊 İşlem Durumu")
                    
                    with gr.Column(scale=1):
                        # Kaydetme bölümü
                        gr.HTML("<h4>💾 Sonuçları Kaydet</h4>")
                        
                        save_image = gr.Image(type="numpy", label="📸 Kaydedilecek Görsel")
                        save_text = gr.Textbox(
                            label="📝 Analiz Sonucu", 
                            lines=4,
                            placeholder="Analiz sonucunu buraya kopyalayın..."
                        )
                        save_notes = gr.Textbox(
                            label="📝 Ek Notlar", 
                            lines=2,
                            placeholder="İsteğe bağlı notlar..."
                        )
                        save_btn = gr.Button("💾 Kaydet", variant="secondary")
                        save_result = gr.Textbox(label="💾 Kaydetme Sonucu")
                
                # Event handlers
                analyze_btn.click(
                    process_image_gradio,
                    inputs=[image_input],
                    outputs=[result_image, analysis_result, status_text]
                )
                
                save_btn.click(
                    save_analysis_gradio,
                    inputs=[save_image, save_text, save_notes],
                    outputs=[save_result]
                )
                
            except ImportError as e:
                gr.HTML(f"<p style='color: red;'>❌ Görsel analiz modülü yüklenemedi: {str(e)}</p>")
        
        with gr.Tab("💬 ChatGPT Benzeri Sohbet"):
            gr.HTML("""
            <div style="text-align: center; padding: 15px; background: #fff8dc; border-radius: 10px; margin-bottom: 15px;">
                <h3>💬 ChatGPT Benzeri AI Sohbet</h3>
                <p>Açık kaynak LLM'ler ile doğal dil sohbeti yapın!</p>
            </div>
            """)
            
            # Sohbet botu arayüzünü içe aktar
            try:
                from chatbot_gradio_interface import (
                    chat_with_bot,
                    analyze_image_and_chat,
                    clear_conversation,
                    get_conversation_list
                )
                
                with gr.Row():
                    with gr.Column(scale=3):                        # Ana sohbet
                        chatbot_display = gr.Chatbot(
                            label="🤖 AI Sohbet Asistanı",
                            height=500,
                            avatar_images=None,
                            bubble_full_width=False
                        )
                        
                        with gr.Row():
                            chat_input = gr.Textbox(
                                label="💬 Mesajınız",
                                placeholder="Merhaba! Size nasıl yardımcı olabilirim?",
                                lines=2,
                                scale=4
                            )
                            chat_send_btn = gr.Button("📤 Gönder", variant="primary", scale=1)
                        
                        with gr.Row():
                            clear_chat_btn = gr.Button("🗑️ Temizle", variant="secondary")
                            history_btn = gr.Button("📋 Geçmiş", variant="secondary")
                    
                    with gr.Column(scale=1):
                        # Bot ayarları
                        bot_type = gr.Radio(
                            ["assistant", "creative", "technical"],
                            value="assistant",
                            label="🤖 Bot Türü"
                        )
                        
                        gr.HTML("""
                        <div style="padding: 15px; background: #f5f5f5; border-radius: 10px; margin-top: 15px;">
                            <h4>🎯 Bot Türleri</h4>
                            <p><b>🤝 Assistant:</b> Genel yardımcı</p>
                            <p><b>🎨 Creative:</b> Yaratıcı yazım</p>
                            <p><b>⚙️ Technical:</b> Teknik destek</p>
                        </div>
                        """)
                        
                        # Konuşma geçmişi
                        conv_history = gr.Textbox(
                            label="📋 Konuşma Geçmişi",
                            lines=8,
                            max_lines=15
                        )
                
                # Event handlers
                chat_send_btn.click(
                    chat_with_bot,
                    inputs=[chat_input, chatbot_display, bot_type],
                    outputs=[chatbot_display, chat_input]
                )
                
                chat_input.submit(
                    chat_with_bot,
                    inputs=[chat_input, chatbot_display, bot_type],
                    outputs=[chatbot_display, chat_input]
                )
                
                clear_chat_btn.click(
                    clear_conversation,
                    outputs=[chatbot_display, chat_input]
                )
                
                history_btn.click(
                    get_conversation_list,
                    outputs=[conv_history]
                )
                
            except ImportError as e:
                gr.HTML(f"<p style='color: red;'>❌ Sohbet botu modülü yüklenemedi: {str(e)}</p>")
        
        with gr.Tab("🔗 Görsel + Sohbet"):
            gr.HTML("""
            <div style="text-align: center; padding: 15px; background: #f0fff0; border-radius: 10px; margin-bottom: 15px;">
                <h3>🔗 Birleşik AI Deneyimi</h3>
                <p>Görsel yükleyin ve hakkında AI ile sohbet edin!</p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Görsel yükleme
                    combined_image = gr.Image(
                        type="numpy",
                        label="📸 Görsel Yükleyin"
                    )
                    
                    combined_question = gr.Textbox(
                        label="❓ Görsel hakkında soru",
                        placeholder="Bu görsel hakkında ne bilmek istiyorsunuz?",
                        lines=3
                    )
                    
                    combined_btn = gr.Button("🔍 Analiz Et & Sor", variant="primary", size="lg")
                
                with gr.Column(scale=2):                    # Birleşik sohbet
                    combined_chatbot = gr.Chatbot(
                        label="🤖 Görsel AI Sohbet",
                        height=500,
                        avatar_images=None
                    )
            
            # Combined event handler
            try:
                combined_btn.click(
                    analyze_image_and_chat,
                    inputs=[combined_image, combined_question, combined_chatbot],
                    outputs=[combined_chatbot, combined_question]
                )
            except:
                gr.HTML("<p style='color: red;'>❌ Birleşik modül yüklenemedi</p>")
        
        with gr.Tab("📊 Sistem Bilgileri"):
            gr.HTML("<h3>🖥️ Sistem Durumu</h3>")
            
            with gr.Row():
                with gr.Column():
                    system_info = gr.HTML()
                    refresh_btn = gr.Button("🔄 Yenile", variant="secondary")
                
                with gr.Column():
                    module_status = gr.HTML()
            
            def get_system_info():
                try:
                    import torch
                    info_html = f"""
                    <div style="padding: 20px; background: #f8f9fa; border-radius: 10px;">
                        <h4>💻 Sistem Bilgileri</h4>
                        <p><b>🐍 Python:</b> {sys.version.split()[0]}</p>
                        <p><b>🔥 PyTorch:</b> {torch.__version__}</p>
                        <p><b>🎮 CUDA:</b> {'✅ Mevcut' if torch.cuda.is_available() else '❌ Mevcut değil'}</p>
                        <p><b>📱 Device:</b> {'GPU' if torch.cuda.is_available() else 'CPU'}</p>
                    </div>
                    """
                    
                    module_html = """
                    <div style="padding: 20px; background: #e8f5e8; border-radius: 10px;">
                        <h4>📦 Modül Durumu</h4>
                        <p>✅ Görsel Analiz Modülü</p>
                        <p>✅ ChatGPT Sohbet Modülü</p>
                        <p>✅ Gradio Arayüz</p>
                        <p>✅ Birleşik AI Hub</p>
                    </div>
                    """
                    
                    return info_html, module_html
                except Exception as e:
                    return f"❌ Sistem bilgisi alınamadı: {str(e)}", "❌ Modül durumu alınamadı"
            
            refresh_btn.click(
                get_system_info,
                outputs=[system_info, module_status]
            )
            
            # Sayfa yüklendiğinde sistem bilgilerini göster
            combined_interface.load(
                get_system_info,
                outputs=[system_info, module_status]
            )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; padding: 20px; margin-top: 30px; background: #f8f9fa; border-radius: 10px;">
            <p><b>🚀 AI Modülleri Hub v2.0</b></p>
            <p>Açık Kaynak LLM'ler & Computer Vision ile Güçlendirildi</p>
            <p style="font-size: 0.9em; color: #666;">
                📸 Görsel Analiz | 💬 ChatGPT Benzeri Sohbet | 🔗 Birleşik AI Deneyimi
            </p>
        </div>
        """)
    
    return combined_interface

def launch_combined_app(
    server_name: str = "0.0.0.0",
    server_port: int = 7862,
    share: bool = False
):
    """
    Birleşik AI uygulamasını başlat
    
    Args:
        server_name (str): Sunucu adı
        server_port (int): Port numarası  
        share (bool): Public link oluştur
    """
    print("🚀 AI Modülleri Hub başlatılıyor...")
    print("📸 Görsel Analiz + 💬 ChatGPT Sohbet")
    
    interface = create_combined_interface()
    
    interface.launch(
        server_name=server_name,
        server_port=server_port,
        share=share,
        show_api=False,
        favicon_path=None
    )

if __name__ == "__main__":
    launch_combined_app()