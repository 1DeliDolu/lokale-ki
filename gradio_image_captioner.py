import gradio as gr
import numpy as np
import os
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
import torch

# Modeli ve işlemciyi yükle
print("🤖 Model yükleniyor...")
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
print("✅ Model başarıyla yüklendi!")

def generate_caption_and_title(input_image: np.ndarray):
    """
    Yüklenen görsel için açıklama ve başlık üretir
    """
    try:
        # NumPy array'ini PIL Image'e çevir
        raw_image = Image.fromarray(input_image).convert('RGB')
        
        # 1. Genel açıklama için işlem
        inputs = processor(images=raw_image, text="a photography of", return_tensors="pt")
        
        # Açıklama üret
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=50, num_beams=5)
        
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        
        # 2. Başlık için daha kısa bir açıklama
        title_inputs = processor(images=raw_image, text="this is", return_tensors="pt")
        
        with torch.no_grad():
            title_outputs = model.generate(**title_inputs, max_length=20, num_beams=3)
        
        title = processor.decode(title_outputs[0], skip_special_tokens=True)
        
        # Sonuçları temizle ve formatla
        caption = caption.replace("a photography of", "").strip()
        title = title.replace("this is", "").strip()
        
        # Başlığı büyük harfle başlat
        title = title.capitalize()
        
        return title, caption, "✅ Analiz tamamlandı!"
        
    except Exception as e:
        return "❌ Hata oluştu", f"Hata: {str(e)}", "❌ Analiz başarısız"

def save_image_with_caption(input_image: np.ndarray, title: str, caption: str):
    """
    Görseli açıklama ve başlıkla birlikte kaydet
    """
    try:
        # Çıktı klasörünü oluştur
        output_dir = "captioned_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # PIL Image'e çevir
        image = Image.fromarray(input_image)
        
        # Dosya adını güvenli hale getir
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        
        # Dosya yolu
        file_path = os.path.join(output_dir, f"{safe_title}.jpg")
        
        # Görseli kaydet
        image.save(file_path, "JPEG", quality=95)
        
        # Açıklama dosyasını kaydet
        caption_file = os.path.join(output_dir, f"{safe_title}_caption.txt")
        with open(caption_file, 'w', encoding='utf-8') as f:
            f.write(f"Başlık: {title}\n")
            f.write(f"Açıklama: {caption}\n")
        
        return f"✅ Görsel kaydedildi: {file_path}"
        
    except Exception as e:
        return f"❌ Kaydetme hatası: {str(e)}"

# Gradio arayüzü
with gr.Blocks(title="🤖 AI Görsel Açıklayıcı ve Başlık Üreteci", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🖼️ Yapay Zeka Görsel Açıklayıcı
    
    Bu uygulama ile:
    - 📸 Görsellerinizi yükleyebilir
    - 🏷️ Otomatik başlık üretebilir  
    - 📝 Detaylı açıklama alabilir
    - 💾 Sonuçları kaydedebilirsiniz
    
    **Nasıl kullanılır:** Aşağıdan bir görsel yükleyin ve "Analiz Et" butonuna tıklayın!
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            # Görsel yükleme alanı
            image_input = gr.Image(
                type="numpy",
                label="📸 Görsel Yükle",
                height=400
            )
            
            # Analiz butonu
            analyze_btn = gr.Button(
                "🔍 Analiz Et", 
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=1):
            # Sonuç alanları
            title_output = gr.Textbox(
                label="🏷️ Üretilen Başlık",
                placeholder="Başlık burada görünecek...",
                interactive=True
            )
            
            caption_output = gr.Textbox(
                label="📝 Görsel Açıklaması",
                placeholder="Açıklama burada görünecek...",
                lines=4,
                interactive=True
            )
            
            status_output = gr.Textbox(
                label="📊 Durum",
                placeholder="Durumu görüntüler..."
            )
            
            # Kaydetme butonu
            save_btn = gr.Button(
                "💾 Kaydet",
                variant="secondary"
            )
            
            save_status = gr.Textbox(
                label="💾 Kaydetme Durumu",
                placeholder="Kaydetme sonucu burada görünecek..."
            )
    
    # Örnek görseller
    gr.Markdown("### 📋 Örnek Görseller")
    gr.Examples(
        examples=[
            ["example_images/cat.jpg"] if os.path.exists("example_images/cat.jpg") else None,
            ["example_images/landscape.jpg"] if os.path.exists("example_images/landscape.jpg") else None,
        ],
        inputs=image_input,
        label="Örnek görselleri deneyin"
    )
    
    # Event handlers
    analyze_btn.click(
        fn=generate_caption_and_title,
        inputs=image_input,
        outputs=[title_output, caption_output, status_output]
    )
    
    save_btn.click(
        fn=save_image_with_caption,
        inputs=[image_input, title_output, caption_output],
        outputs=save_status
    )
    
    # Footer
    gr.Markdown("""
    ---
    💡 **İpucu:** Sonuçları beğenmediyseniz, başlık ve açıklama kutularını düzenleyebilir, 
    ardından "Kaydet" butonuna tıklayabilirsiniz.
    
    🔧 **Kullanılan Model:** Salesforce/blip-image-captioning-base
    """)

# Uygulamayı başlat
if __name__ == "__main__":
    print("🚀 Gradio uygulaması başlatılıyor...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )