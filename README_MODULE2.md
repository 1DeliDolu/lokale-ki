# 🤖 AI Modülleri Hub - Tam Donanımlı Yapay Zeka Uygulamaları

Bu proje, **Modül 2: ChatGPT Benzeri Web Sitesi** kapsamında geliştirilmiş tam donanımlı bir AI hub'ıdır.

## 🎯 Özellikler

### 📸 Modül 1: AI Görsel Açıklayıcı
- **Otomatik Görsel Analiz**: BLIP modeli ile görsel açıklama
- **Başlık Üretme**: Akıllı başlık önerileri
- **Metadata Kaydetme**: Analiz sonuçlarını kaydetme
- **Çoklu Format Desteği**: JPG, PNG, GIF, BMP

### 💬 Modül 2: ChatGPT Benzeri Sohbet Botu
- **Açık Kaynak LLM'ler**: DialoGPT ve GPT-2 modelleri
- **Çoklu Bot Türleri**: Asistan, Yaratıcı, Teknik uzman
- **Konuşma Geçmişi**: Otomatik kayıt ve yönetim
- **Türkçe Dil Desteği**: Özel Türkçe optimizasyonları

### 🔗 Birleşik AI Deneyimi
- **Görsel + Sohbet**: Görsel yükleyip hakkında konuşma
- **Tek Arayüz**: Tüm özellikler bir arada
- **Gradio Web UI**: Modern ve kullanıcı dostu arayüz

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler

```bash
# Temel gereksinimler
pip install -r requirements.txt

# ChatGPT modülü için ek gereksinimler  
pip install -r requirements_chatbot.txt

# Görsel analiz için (zaten yüklü)
pip install -r requirements_gradio.txt
```

### 2. Uygulamaları Çalıştırma

#### 🔗 Tüm Modüller (Önerilen)
```bash
python run_combined_ai.py
# http://localhost:7862
```

#### 📸 Sadece Görsel Analiz
```bash
python run_app.py  
# http://localhost:7860
```

#### 💬 Sadece ChatGPT Sohbet
```bash
python run_chatbot.py
# http://localhost:7861
```

## 📦 Modül Yapısı

```
lokale-ki/
├── 📸 image_analysis/          # Görsel analiz modülü
│   ├── __init__.py
│   ├── analyzer.py             # Ana analiz sınıfı
│   ├── config.py               # Konfigürasyonlar
│   ├── utils.py                # Yardımcı fonksiyonlar
│   └── exceptions.py           # Özel hata sınıfları
├── 💬 chatbot_module/          # ChatGPT benzeri sohbet
│   ├── __init__.py
│   ├── chatbot.py              # Ana sohbet botu
│   ├── config.py               # Bot konfigürasyonları
│   ├── utils.py                # Sohbet yardımcıları
│   └── exceptions.py           # Sohbet hataları
├── 🌐 Web Arayüzleri
│   ├── gradio_interface.py     # Görsel analiz UI
│   ├── chatbot_gradio_interface.py  # Sohbet UI
│   └── run_combined_ai.py      # Birleşik UI
└── 🚀 Başlatıcılar
    ├── run_app.py              # Görsel analiz app
    ├── run_chatbot.py          # Sohbet app
    └── run_combined_ai.py      # Birleşik app
```

## 🤖 ChatGPT Benzeri Sohbet Botu Özellikleri

### Bot Türleri

#### 🤝 Yardımcı Asistan (Assistant)
- Genel sorular ve yardım
- Bilgilendirici yanıtlar
- Günlük konuşmalar

#### 🎨 Yaratıcı Yazar (Creative)
- Hikaye yazma
- Şiir ve yaratıcı metinler
- Beyin fırtınası

#### ⚙️ Teknik Uzman (Technical)
- Programlama soruları
- Teknik açıklamalar
- Kod örnekleri

### Kullanılan Modeller

- **microsoft/DialoGPT-medium**: Ana konuşma modeli
- **microsoft/DialoGPT-large**: Gelişmiş yanıtlar için
- **microsoft/DialoGPT-small**: Hızlı yanıtlar için

## 🧪 Test ve Geliştirme

### ChatGPT Modülü Test
```bash
python test_chatbot.py
```

### Görsel Analiz Test  
```bash
python test_module.py
```

## 🔧 Konfigürasyon

### ChatBot Ayarları
```python
from chatbot_module import ChatbotConfig, ModelPresets

# Özel konfigürasyon
config = ChatbotConfig(
    model_name="microsoft/DialoGPT-medium",
    temperature=0.8,
    max_new_tokens=150
)

# Hazır presetler
assistant_config = ModelPresets.helpful_assistant()
creative_config = ModelPresets.creative_writer()
```

### Görsel Analiz Ayarları
```python
from image_analysis import AnalysisConfig, ModelConfig

# Model ayarları
model_config = ModelConfig(
    model_name="Salesforce/blip-image-captioning-base"
)

# Analiz ayarları  
analysis_config = AnalysisConfig(
    save_metadata=True,
    output_format="JPEG"
)
```

## 🎓 Eğitim Modülü: Modül 2

Bu proje, **"Kendi ChatGPT Benzeri Web Siteni Oluştur"** eğitim modülünün tam uygulamasıdır.

### 📚 Öğrenilen Konular

1. **Açık Kaynak LLM'ler**
   - Hugging Face Transformers
   - DialoGPT modelleri
   - Model fine-tuning

2. **Web Arayüz Geliştirme**
   - Gradio framework
   - Responsive design
   - Multi-tab arayüzler

3. **Konuşma Yönetimi**
   - Session management
   - Conversation history
   - Context awareness

4. **AI Entegrasyonu**
   - Model loading
   - GPU optimization
   - Error handling

## 🌟 Gelişmiş Özellikler

### 🔐 Güvenlik
- Input validation
- Sanitization
- Rate limiting (isteğe bağlı)

### ⚡ Performans
- Model caching
- Lazy loading
- Memory optimization

### 🌍 Çoklu Dil
- Türkçe optimizasyonu
- Dil tespiti
- Uygun yanıt formatı

### 💾 Veri Yönetimi
- JSON tabanlı depolama
- Conversation backup
- Export/import

## 🚀 Prodüksiyon Hazırlığı

### Docker Kurulumu
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements*.txt ./
RUN pip install -r requirements.txt
RUN pip install -r requirements_chatbot.txt

COPY . .
EXPOSE 7862

CMD ["python", "run_combined_ai.py"]
```

### Environment Variables
```bash
export TORCH_HOME=/path/to/models
export HF_HOME=/path/to/huggingface
export GRADIO_SERVER_NAME=0.0.0.0
export GRADIO_SERVER_PORT=7862
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun
3. Değişiklikleri commit edin
4. Pull request gönderin

## 📄 Lisans

MIT License - Detaylar için `LICENSE` dosyasına bakın.

## 🆘 Destek

- **Issues**: GitHub issues sayfasından
- **Dokumentasyon**: Bu README dosyası
- **Test Dosyaları**: `test_*.py` dosyalarına bakın

---

### 🎉 Modül 2 Tamamlandı!

✅ ChatGPT benzeri sohbet botu oluşturuldu  
✅ Açık kaynak LLM'ler entegre edildi  
✅ Web arayüzü geliştirildi  
✅ Görsel analiz ile birleştirildi  
✅ Production-ready kod yapısı

**Sonraki Modül**: 🗣️ Sesli Asistan Geliştirme