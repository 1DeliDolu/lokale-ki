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

def generate_caption_and_title(input_image):
    """
    Yüklenen görsel için açıklama ve başlık üretir
    """
    try:
        # Input kontrolü
        if input_image is None:
            return "❌ Görsel yok", "Lütfen bir görsel yükleyin", "❌ Görsel seçilmedi"
        
        # PIL Image'e çevir
        if isinstance(input_image, np.ndarray):
            raw_image = Image.fromarray(input_image.astype('uint8')).convert('RGB')
        else:
            raw_image = input_image.convert('RGB')
        
        # Görsel boyutunu kontrol et ve gerekirse yeniden boyutlandır
        max_size = 512
        if max(raw_image.size) > max_size:
            raw_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        print(f"📸 İşlenen görsel boyutu: {raw_image.size}")
        
        # 1. Genel açıklama için işlem
        inputs = processor(images=raw_image, return_tensors="pt")
        
        # Açıklama üret - daha güvenli parametreler
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_length=50, 
                num_beams=2,
                do_sample=False,
                early_stopping=True
            )
        
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        
        # 2. Başlık için koşullu metin ile
        conditional_inputs = processor(images=raw_image, text="a photo of", return_tensors="pt")
        
        with torch.no_grad():
            title_outputs = model.generate(
                **conditional_inputs, 
                max_length=30, 
                num_beams=2,
                do_sample=False,
                early_stopping=True
            )
        
        title = processor.decode(title_outputs[0], skip_special_tokens=True)
        
        # Sonuçları temizle ve formatla
        caption = caption.strip()
        title = title.replace("a photo of", "").strip()
        
        # Başlığı büyük harfle başlat ve kısalt
        title = title.capitalize()
        if len(title) > 50:
            title = title[:50] + "..."
        
        print(f"✅ Başlık: {title}")
        print(f"✅ Açıklama: {caption}")
        
        return title, caption, "✅ Analiz tamamlandı!"
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Hata: {error_msg}")
        return "❌ Analiz hatası", f"Hata detayı: {error_msg}", "❌ İşlem başarısız"

def save_image_with_caption(input_image, title, caption):
    """
    Görseli açıklama ve başlıkla birlikte kaydet
    """
    try:
        if input_image is None:
            return "❌ Kaydedilecek görsel yok"
        
        # Çıktı klasörünü oluştur
        output_dir = "captioned_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # PIL Image'e çevir
        if isinstance(input_image, np.ndarray):
            image = Image.fromarray(input_image.astype('uint8'))
        else:
            image = input_image
        
        # RGB'ye çevir
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Dosya adını güvenli hale getir
        import re
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        if not safe_title or len(safe_title) < 3:
            safe_title = "image_caption"
        
        # Dosya yolu
        file_path = os.path.join(output_dir, f"{safe_title}.jpg")
        
        # Eğer dosya varsa sayı ekle
        counter = 1
        original_path = file_path
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_path)
            file_path = f"{name}_{counter}{ext}"
            counter += 1
        
        # Görseli kaydet
        image.save(file_path, "JPEG", quality=95, optimize=True)
        
        # Açıklama dosyasını kaydet
        caption_file = file_path.replace('.jpg', '_caption.txt')
        with open(caption_file, 'w', encoding='utf-8') as f:
            f.write(f"Başlık: {title}\n")
            f.write(f"Açıklama: {caption}\n")
            f.write(f"Kayıt Tarihi: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        return f"✅ Görsel kaydedildi: {os.path.basename(file_path)}"
        
    except Exception as e:
        print(f"❌ Kaydetme hatası: {str(e)}")
        return f"❌ Kaydetme hatası: {str(e)}"

# Gradio arayüzü - Basit Interface kullanarak
def process_image(image):
    """Basit işlem fonksiyonu"""
    if image is None:
        return None, "Lütfen bir görsel yükleyin", "❌ Görsel yok"
    
    title, caption, status = generate_caption_and_title(image)
    return image, f"📝 Başlık: {title}\n\n🔍 Açıklama: {caption}", status

# Gradio Interface
demo = gr.Interface(
    fn=process_image,
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
    """,
    examples=[
        # Örnek görseller varsa buraya ekleyebilirsiniz
    ],
    allow_flagging="never",
    theme="default"
)

# Uygulamayı başlat
if __name__ == "__main__":
    print("🚀 Gradio uygulaması başlatılıyor...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )