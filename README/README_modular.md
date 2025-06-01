# 🤖 AI Görsel Açıklayıcı - Modüler Versiyon

Bu proje, yapay zeka kullanarak görselleri analiz eden ve açıklama üreten modüler bir uygulamadır.

## 📁 Dosya Yapısı

```
lokale-ki/
├── image_analyzer.py      # 🧠 Görsel analiz motoru
├── gradio_interface.py    # 🎨 Web arayüzü
├── run_app.py            # 🚀 Ana başlatıcı
├── cli_analyzer.py       # 💻 Komut satırı arayüzü
├── requirements_gradio.txt # 📦 Gerekli paketler
└── captioned_images/     # 📸 Çıktı klasörü
```

## 🚀 Kurulum

1. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements_gradio.txt
```

## 🎯 Kullanım Yöntemleri

### 1. 🌐 Web Arayüzü (Gradio)
```bash
python run_app.py
```
- Tarayıcıda `http://localhost:7860` açılır
- Drag & drop ile görsel yükleme
- İki sekme: Analiz ve Kaydetme

### 2. 💻 Komut Satırı
```bash
# Tek görsel analizi
python cli_analyzer.py image.jpg

# Analiz et ve kaydet
python cli_analyzer.py image.jpg --save

# Klasör analizi
python cli_analyzer.py --folder ./images

# Klasör analizi + kaydetme
python cli_analyzer.py --folder ./images --save
```

### 3. 🐍 Python Kodu Olarak
```python
from image_analyzer import ImageAnalyzer

# Analyzer oluştur
analyzer = ImageAnalyzer()

# Tek görsel analizi
result = analyzer.analyze_image("image.jpg")
print(f"Başlık: {result['title']}")
print(f"Açıklama: {result['caption']}")

# Kaydetme
analyzer.save_image_with_metadata(
    "image.jpg", 
    result['title'], 
    result['caption']
)
```

## ⚙️ Modül Detayları

### 🧠 ImageAnalyzer (`image_analyzer.py`)
- **Temel fonksiyonlar:**
  - `analyze_image()` - Görsel analizi
  - `generate_title()` - Başlık üretimi
  - `generate_caption()` - Açıklama üretimi
  - `save_image_with_metadata()` - Kaydetme
  - `batch_analyze()` - Toplu analiz

### 🎨 Gradio Interface (`gradio_interface.py`)
- **İki sekme:**
  - Görsel Analizi - Upload → Analiz → Sonuç
  - Sonuç Kaydetme - Metadata ile kaydetme
- **Özellikler:**
  - Drag & drop desteği
  - Canlı önizleme
  - Hata yönetimi

### 💻 CLI Analyzer (`cli_analyzer.py`)
- **Komut satırı seçenekleri:**
  - Tek dosya analizi
  - Klasör analizi
  - Otomatik kaydetme
  - İlerleme gösterimi

## 📊 Çıktı Formatları

### 🖼️ Görsel Dosyası
- Format: JPEG (95% kalite)
- Maksimum boyut: 512px (otomatik resize)

### 📄 Metadata Dosyası
```
Dosya: image.jpg
Başlık: Beautiful sunset landscape
Açıklama: a beautiful sunset over a mountain landscape with trees
Model: Salesforce/blip-image-captioning-base
Analiz Tarihi: 2024-01-15 14:30:25
```

## 🔧 Özelleştirme

### Model Değiştirme
```python
# Farklı model kullanma
analyzer = ImageAnalyzer("Salesforce/blip2-opt-2.7b")
```

### Çıktı Klasörü
```python
# Özel çıktı klasörü
analyzer.save_image_with_metadata(
    image, title, caption, 
    output_dir="my_custom_folder"
)
```

## 🎯 Kullanım Senaryoları

- 📁 **Fotoğraf Arşivleme** - Binlerce fotoğrafı otomatik etiketleme
- 📱 **Sosyal Medya** - Paylaşım için otomatik açıklama
- ♿ **Erişilebilirlik** - Görme engelliler için alt metin
- 🏢 **İş Süreçleri** - Döküman ve görsel kataloglama
- 🎓 **Eğitim** - Görsel içerik analizi

## 🛠️ Geliştirici Notları

- **Model:** Salesforce BLIP (Bootstrapped Language-Image Pre-training)
- **Framework:** Hugging Face Transformers
- **UI:** Gradio 3.50.2 (stabil versiyon)
- **Image Processing:** PIL/Pillow
- **CLI:** argparse

## 📈 Performans

- **İlk yükleme:** 1-2 dakika (model indirme)
- **Analiz süresi:** 2-5 saniye/görsel
- **Bellek kullanımı:** ~2GB (GPU) / ~4GB (CPU)
- **Desteklenen formatlar:** JPG, PNG, GIF, BMP

## 🐛 Sorun Giderme

1. **Model yükleme hatası:**
   ```bash
   pip install --upgrade transformers torch
   ```

2. **Gradio versiyonu sorunu:**
   ```bash
   pip install gradio==3.50.2 pydantic==1.10.13
   ```

3. **Bellek hatası:**
   - Görsel boyutunu küçültün
   - Batch boyutunu azaltın
   - GPU kullanın (varsa)