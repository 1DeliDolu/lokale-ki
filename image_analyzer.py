import numpy as np
import os
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
import torch
import re
from datetime import datetime

class ImageAnalyzer:
    """
    Görsel analizi ve açıklama üretimi için sınıf
    """
    
    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        """
        Model ve işlemciyi yükle
        """
        print("🤖 Model yükleniyor...")
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        self.model_name = model_name
        print("✅ Model başarıyla yüklendi!")
    
    def preprocess_image(self, input_image, max_size=512):
        """
        Görseli işleme için hazırla
        """
        try:
            # PIL Image'e çevir
            if isinstance(input_image, np.ndarray):
                raw_image = Image.fromarray(input_image.astype('uint8')).convert('RGB')
            elif isinstance(input_image, str):  # Dosya yolu
                raw_image = Image.open(input_image).convert('RGB')
            else:
                raw_image = input_image.convert('RGB')
            
            # Görsel boyutunu kontrol et ve gerekirse yeniden boyutlandır
            if max(raw_image.size) > max_size:
                raw_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            print(f"📸 İşlenen görsel boyutu: {raw_image.size}")
            return raw_image
            
        except Exception as e:
            print(f"❌ Görsel işleme hatası: {str(e)}")
            return None
    
    def generate_caption(self, image, conditional_text=""):
        """
        Görsel için açıklama üret
        """
        try:
            # Görsel işleme
            processed_image = self.preprocess_image(image)
            if processed_image is None:
                return "❌ Görsel işlenemedi"
            
            # Model girişi hazırla
            if conditional_text:
                inputs = self.processor(images=processed_image, text=conditional_text, return_tensors="pt")
            else:
                inputs = self.processor(images=processed_image, return_tensors="pt")
            
            # Açıklama üret
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs, 
                    max_length=50, 
                    num_beams=2,
                    do_sample=False,
                    early_stopping=True
                )
            
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            
            # Koşullu metni temizle
            if conditional_text:
                caption = caption.replace(conditional_text, "").strip()
            
            return caption.strip()
            
        except Exception as e:
            error_msg = f"Açıklama üretme hatası: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def generate_title(self, image):
        """
        Görsel için başlık üret
        """
        try:
            title = self.generate_caption(image, "a photo of")
            
            # Başlığı formatla
            title = title.capitalize()
            if len(title) > 50:
                title = title[:50] + "..."
            
            return title if title else "Untitled"
            
        except Exception as e:
            print(f"❌ Başlık üretme hatası: {str(e)}")
            return "Untitled"
    
    def analyze_image(self, image):
        """
        Görsel için hem başlık hem açıklama üret
        """
        try:
            if image is None:
                return {
                    'title': "❌ Görsel yok",
                    'caption': "Lütfen bir görsel yükleyin",
                    'status': "❌ Görsel seçilmedi",
                    'success': False
                }
            
            # Başlık üret
            title = self.generate_title(image)
            
            # Açıklama üret
            caption = self.generate_caption(image)
            
            print(f"✅ Başlık: {title}")
            print(f"✅ Açıklama: {caption}")
            
            return {
                'title': title,
                'caption': caption,
                'status': "✅ Analiz tamamlandı!",
                'success': True
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Analiz hatası: {error_msg}")
            return {
                'title': "❌ Analiz hatası",
                'caption': f"Hata detayı: {error_msg}",
                'status': "❌ İşlem başarısız",
                'success': False
            }
    
    def save_image_with_metadata(self, image, title, caption, output_dir="captioned_images"):
        """
        Görseli metadata ile birlikte kaydet
        """
        try:
            if image is None:
                return "❌ Kaydedilecek görsel yok"
            
            # Çıktı klasörünü oluştur
            os.makedirs(output_dir, exist_ok=True)
            
            # PIL Image'e çevir
            if isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image.astype('uint8'))
            else:
                pil_image = image
            
            # RGB'ye çevir
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Güvenli dosya adı oluştur
            safe_title = self._create_safe_filename(title)
            
            # Dosya yolu
            file_path = os.path.join(output_dir, f"{safe_title}.jpg")
            
            # Dosya çakışmasını önle
            file_path = self._get_unique_filepath(file_path)
            
            # Görseli kaydet
            pil_image.save(file_path, "JPEG", quality=95, optimize=True)
            
            # Metadata dosyasını kaydet
            self._save_metadata(file_path, title, caption)
            
            return f"✅ Görsel kaydedildi: {os.path.basename(file_path)}"
            
        except Exception as e:
            error_msg = f"Kaydetme hatası: {str(e)}"
            print(f"❌ {error_msg}")
            return f"❌ {error_msg}"
    
    def _create_safe_filename(self, title):
        """
        Güvenli dosya adı oluştur
        """
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        if not safe_title or len(safe_title) < 3:
            safe_title = "image_caption"
        return safe_title
    
    def _get_unique_filepath(self, file_path):
        """
        Benzersiz dosya yolu oluştur
        """
        counter = 1
        original_path = file_path
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_path)
            file_path = f"{name}_{counter}{ext}"
            counter += 1
        return file_path
    
    def _save_metadata(self, image_path, title, caption):
        """
        Metadata dosyasını kaydet
        """
        metadata_file = image_path.replace('.jpg', '_metadata.txt')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(f"Dosya: {os.path.basename(image_path)}\n")
            f.write(f"Başlık: {title}\n")
            f.write(f"Açıklama: {caption}\n")
            f.write(f"Model: {self.model_name}\n")
            f.write(f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def batch_analyze(self, image_paths):
        """
        Birden fazla görseli toplu analiz et
        """
        results = []
        
        for i, image_path in enumerate(image_paths):
            print(f"📸 Analiz ediliyor ({i+1}/{len(image_paths)}): {os.path.basename(image_path)}")
            
            try:
                result = self.analyze_image(image_path)
                result['file_path'] = image_path
                results.append(result)
                
            except Exception as e:
                print(f"❌ Hata: {image_path} - {str(e)}")
                results.append({
                    'file_path': image_path,
                    'title': "❌ Hata",
                    'caption': str(e),
                    'status': "❌ Başarısız",
                    'success': False
                })
        
        return results

# Test ve kullanım örneği
if __name__ == "__main__":
    # Analyzer oluştur
    analyzer = ImageAnalyzer()
    
    # Test görseli (varsa)
    test_image_path = "test_image.jpg"
    if os.path.exists(test_image_path):
        result = analyzer.analyze_image(test_image_path)
        print("\n📊 Analiz Sonucu:")
        print(f"Başlık: {result['title']}")
        print(f"Açıklama: {result['caption']}")
        print(f"Durum: {result['status']}")
    else:
        print("ℹ️ Test görseli bulunamadı. Gradio arayüzünü kullanın.")