import gradio as gr
from image_analysis import ImageAnalyzer, ModelConfig, AnalysisConfig
import os

# Global analyzer nesnesi
analyzer = None

def initialize_analyzer():
    """
    Analyzer'ı başlat
    """
    global analyzer
    if analyzer is None:
        analyzer = ImageAnalyzer()
    return analyzer

def process_image_gradio(image):
    """
    Gradio için görsel işleme fonksiyonu
    """
    try:
        # Analyzer'ı başlat
        current_analyzer = initialize_analyzer()
        
        if image is None:
            return None, "Lütfen bir görsel yükleyin", "❌ Görsel yok"
        
        # Görseli analiz et
        result = current_analyzer.analyze_image(image)
        
        # Sonuçları formatla
        formatted_result = f"📝 **Başlık:** {result['title']}\n\n🔍 **Açıklama:** {result['caption']}"
        
        return image, formatted_result, result['status']
        
    except Exception as e:
        error_msg = f"Gradio işleme hatası: {str(e)}"
        print(f"❌ {error_msg}")
        return None, error_msg, "❌ Hata oluştu"

def save_analysis_gradio(image, title_text, caption_text):
    """
    Analiz sonuçlarını kaydet
    """
    try:
        current_analyzer = initialize_analyzer()
        
        if image is None:
            return "❌ Kaydedilecek görsel yok"
        
        # Başlık ve açıklamayı parse et
        lines = title_text.split('\n')
        title = ""
        caption = ""
        
        for line in lines:
            if "**Başlık:**" in line:
                title = line.replace("📝 **Başlık:**", "").strip()
            elif "**Açıklama:**" in line:
                caption = line.replace("🔍 **Açıklama:**", "").strip()
        
        if not title:
            title = "Untitled"
        if not caption:
            caption = "No description"
        
        # Kaydet
        result = current_analyzer.save_image_with_metadata(image, title, caption)
        return result
        
    except Exception as e:
        return f"❌ Kaydetme hatası: {str(e)}"

def create_gradio_interface():
    """
    Gradio arayüzünü oluştur
    """
    
    # Ana işlem arayüzü
    main_interface = gr.Interface(
        fn=process_image_gradio,
        inputs=gr.Image(type="numpy", label="📸 Görselinizi Yükleyin"),
        outputs=[
            gr.Image(type="numpy", label="📷 Yüklenen Görsel"),
            gr.Textbox(label="🤖 AI Analiz Sonucu", lines=5),
            gr.Textbox(label="📊 İşlem Durumu")
        ],
        title="🖼️ AI Görsel Açıklayıcı",
        description="""
        ### 🚀 Nasıl Kullanılır?
        1. **Görsel Yükle:** Bir fotoğraf seçin veya sürükleyip bırakın
        2. **Analiz Et:** "Submit" butonuna tıklayın  
        3. **Sonucu Gör:** AI'ın ürettiği başlık ve açıklamayı görün
        
        **Desteklenen Formatlar:** JPG, PNG, GIF, BMP
        **Model:** Salesforce BLIP Image Captioning
        """,        allow_flagging="never",
        theme=gr.themes.Soft(),  # Yerleşik tema kullan
        api_name="analyze"
    )
    
    # Kaydetme arayüzü
    save_interface = gr.Interface(
        fn=save_analysis_gradio,
        inputs=[
            gr.Image(type="numpy", label="📸 Kaydedilecek Görsel"),
            gr.Textbox(label="📝 Analiz Sonucu", lines=5, placeholder="Analiz sonucunu buraya yapıştırın..."),
            gr.Textbox(label="📝 Ek Notlar", lines=2, placeholder="İsteğe bağlı ek notlar...")
        ],
        outputs=gr.Textbox(label="💾 Kaydetme Sonucu"),
        title="💾 Analiz Sonuçlarını Kaydet",
        description="""
        ### 📁 Sonuçları Kaydetme
        1. **Görseli yükleyin** ve **analiz sonucunu yapıştırın**
        2. **Submit** butonuna tıklayın
        3. Dosyalar `captioned_images/` klasörüne kaydedilir
        
        **Kaydedilen Dosyalar:**
        - `baslik.jpg` - Görsel dosyası
        - `baslik_metadata.txt` - Analiz detayları
        """,
        allow_flagging="never",
        api_name="save"
    )
    
    # Tab'lar ile birleştir
    tabbed_interface = gr.TabbedInterface(
        [main_interface, save_interface],
        ["🔍 Görsel Analizi", "💾 Sonuç Kaydetme"],
        title="🤖 AI Görsel Açıklayıcı - Tam Versiyon"
    )
    
    return tabbed_interface

def launch_gradio_app(server_name="0.0.0.0", server_port=7860, share=False):
    """
    Gradio uygulamasını başlat
    """
    print("🚀 Gradio uygulaması başlatılıyor...")
    
    # Arayüzü oluştur
    demo = create_gradio_interface()
    
    # Uygulamayı başlat
    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=share,
        show_error=True
    )

# Ana çalıştırma
if __name__ == "__main__":
    # Çıktı klasörünü oluştur
    os.makedirs("captioned_images", exist_ok=True)
    
    print("🎯 AI Görsel Açıklayıcı Gradio Arayüzü")
    print("=" * 50)
    
    # Uygulamayı başlat
    launch_gradio_app()