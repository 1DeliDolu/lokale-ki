# 💬 ChatGPT Benzeri Sohbet Botu - Kullanım Kılavuzu

Bu kılavuz, Modül 2 kapsamında geliştirilen ChatGPT benzeri sohbet botunun detaylı kullanım talimatlarını içerir.

## 🎯 Genel Bakış

ChatGPT benzeri sohbet botu, açık kaynak Large Language Models (LLM) kullanarak doğal dil konuşması yapabilen bir AI asistanıdır.

### 🌟 Ana Özellikler

- **Çoklu Bot Kişiliği**: 3 farklı uzman bot türü
- **Konuşma Geçmişi**: Otomatik kayıt ve sürdürme
- **Türkçe Dil Desteği**: Özel optimizasyonlar
- **Web Arayüzü**: Modern Gradio tabanlı UI
- **Görsel Entegrasyon**: Resimleri analiz edip tartışma

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Gerekli paketleri yükleyin
pip install -r requirements_chatbot.txt

# Uygulamayı başlatın
python run_chatbot.py
```

### 2. Web Arayüzüne Erişim

Tarayıcınızda şu adresi açın: <http://localhost:7861>

## 🤖 Bot Türleri

### 🤝 Yardımcı Asistan (Assistant)

**Kullanım Alanları:**

- Genel bilgi ve yardım
- Günlük konular
- Basit sorular
- Açıklama istekleri

**Örnek Konuşmalar:**

```text
Kullanıcı: Python nedir?
Bot: Python, kolay öğrenilebilir ve güçlü bir programlama dilidir...

Kullanıcı: Bugün nasıl bir gün?
Bot: Size nasıl yardımcı olabilirim? Hangi konuda bilgi almak istiyorsunuz?
```

### 🎨 Yaratıcı Yazar (Creative)

**Kullanım Alanları:**

- Hikaye yazma
- Şiir oluşturma
- Yaratıcı fikirler
- Beyin fırtınası

**Örnek Konuşmalar:**

```text
Kullanıcı: Kısa bir hikaye yaz
Bot: Bir zamanlar, uzak bir şehirde yaşayan genç bir mucit...

Kullanıcı: Yaz hakkında bir şiir yaz
Bot: Güneşin altında altın yapraklar, sıcak rüzgarın getirdiği...
```

### ⚙️ Teknik Uzman (Technical)

**Kullanım Alanları:**

- Programlama soruları
- Teknik açıklamalar
- Kod örnekleri
- Sistem yönetimi

**Örnek Konuşmalar:**

```text
Kullanıcı: Python'da liste nasıl oluşturulur?
Bot: Python'da liste oluşturmak için köşeli parantez kullanılır...

Kullanıcı: API nedir?
Bot: API (Application Programming Interface), uygulamalar arası...
```

## 📱 Web Arayüzü Kullanımı

### 💬 Ana Sohbet Sekmesi

1. **Mesaj Yazma**
   - Alt kısımdaki metin kutusuna mesajınızı yazın
   - "Gönder" butonuna tıklayın veya Enter tuşuna basın

2. **Bot Türü Seçimi**
   - Sağ panelden istediğiniz bot türünü seçin
   - Her bot farklı kişilik ve uzmanlık alanına sahiptir

3. **Konuşma Yönetimi**
   - "Temizle" butonu: Mevcut konuşmayı sıfırlar
   - "Geçmiş" butonu: Önceki konuşmaları gösterir

### 📸 Görsel + Sohbet Sekmesi

1. **Görsel Yükleme**
   - Sol panelden bir görsel yükleyin
   - JPG, PNG, GIF formatları desteklenir

2. **Görsel Hakkında Soru Sorma**
   - Görsel ile ilgili spesifik soru yazın
   - Veya boş bırakarak genel analiz isteyin

3. **Analiz ve Tartışma**
   - Bot önce görseli analiz eder
   - Sonra sorunuza göre detaylı açıklama yapar

### 📊 İstatistikler Sekmesi

- Model bilgileri
- Sistem durumu
- Konuşma geçmişi listesi
- Performans metrikleri

## 🔧 Gelişmiş Özellikler

### Konuşma Geçmişi

Bot, her konuşmayı otomatik olarak kaydeder:

```python
# Konuşma listesi
conversations = bot.get_conversation_list()

# Belirli bir konuşmayı getir
conversation = bot.get_conversation("conv_id")

# Yeni konuşma başlat
new_conv_id = bot.start_new_conversation("Yeni Konu")
```

### Özel Bot Konfigürasyonu

```python
from chatbot_module import ChatbotConfig, ChatGPTLikeBot

# Özel ayarlar
config = ChatbotConfig(
    model_name="microsoft/DialoGPT-medium",
    temperature=0.7,          # Yaratıcılık seviyesi (0.1-1.0)
    max_new_tokens=200,       # Maksimum yanıt uzunluğu
    repetition_penalty=1.1    # Tekrar önleme
)

# Bot oluştur
custom_bot = ChatGPTLikeBot(config)
response = custom_bot.chat("Merhaba!")
```

## 🎛️ Parametreler ve Ayarlar

### Temel Parametreler

| Parametre | Açıklama | Varsayılan | Aralık |
|-----------|----------|------------|---------|
| `temperature` | Yaratıcılık/rastgelelik | 0.8 | 0.1-1.0 |
| `max_new_tokens` | Yanıt uzunluğu | 150 | 50-500 |
| `top_p` | Kelime seçim çeşitliliği | 0.9 | 0.1-1.0 |
| `repetition_penalty` | Tekrar önleme | 1.1 | 1.0-1.5 |

### Bot Türü Presetleri

```python
from chatbot_module import ModelPresets

# Hazır konfigürasyonlar
assistant = ModelPresets.helpful_assistant()    # Dengeli
creative = ModelPresets.creative_writer()       # Yaratıcı  
technical = ModelPresets.technical_expert()     # Teknik
fast = ModelPresets.fast_chat()                 # Hızlı
```

## 💡 İpuçları ve En İyi Uygulamalar

### Etkili Sohbet İçin

1. **Açık ve Net Sorular Sorun**
   ```text
   ❌ "Bir şey sor"
   ✅ "Python programlama dili hakkında bilgi ver"
   ```

2. **Bağlam Sağlayın**
   ```text
   ❌ "Bu nasıl yapılır?"
   ✅ "Python'da liste elemanlarını nasıl sıralarım?"
   ```

3. **Uygun Bot Türü Seçin**
   - Teknik sorular → Technical Bot
   - Yaratıcı görevler → Creative Bot
   - Genel konular → Assistant Bot

### Performans Optimizasyonu

1. **Model Seçimi**
   - Hızlı yanıt: `DialoGPT-small`
   - Dengeli: `DialoGPT-medium`
   - En iyi kalite: `DialoGPT-large`

2. **Parametre Ayarı**
   - Hızlı yanıt: `temperature=0.5, max_new_tokens=80`
   - Detaylı yanıt: `temperature=0.8, max_new_tokens=200`

## 🔧 Sorun Giderme

### Yaygın Sorunlar

1. **Model Yükleme Hatası**
   ```bash
   # Çözüm: Cache temizle
   rm -rf ~/.cache/huggingface/
   python run_chatbot.py
   ```

2. **Yavaş Yanıt**
   ```python
   # Küçük model kullan
   config = ModelPresets.fast_chat()
   ```

3. **Bağlantı Hatası**
   ```bash
   # Port kontrolü
   netstat -an | grep 7861
   # Farklı port dene
   python run_chatbot.py --port 7862
   ```

### Hata Mesajları

| Hata | Sebep | Çözüm |
|------|-------|-------|
| `ModelLoadError` | Model bulunamadı | Cache temizle, yeniden indir |
| `ConversationError` | Konuşma hatası | Yeni konuşma başlat |
| `GenerationTimeoutError` | Zaman aşımı | Daha kısa sorular sor |

## 📚 Gelişmiş Kullanım

### Programatik Kullanım

```python
from chatbot_module import ChatGPTLikeBot, ConversationManager

# Basit kullanım
bot = ChatGPTLikeBot()
response = bot.chat("Merhaba!")

# Çoklu bot yönetimi
manager = ConversationManager()
manager.create_bot("bot1", ModelPresets.helpful_assistant())
response = manager.chat_with_bot("bot1", "Selam!")

# Konuşma geçmişi ile
conv_id = bot.start_new_conversation("AI Sohbeti")
response1 = bot.chat("Python nedir?", conv_id)
response2 = bot.chat("Örneklerle açıkla", conv_id)  # Bağlamı hatırlar
```

### Batch İşleme

```python
# Çoklu soru işleme
questions = [
    "Python nedir?",
    "Nasıl öğrenirim?",
    "Hangi projelerde kullanılır?"
]

for q in questions:
    response = bot.chat(q)
    print(f"S: {q}")
    print(f"C: {response}\n")
```

## 🌐 API Entegrasyonu

### REST API Kullanımı

```python
import requests

# API endpoint
url = "http://localhost:7861/api/predict"

# Mesaj gönder
data = {
    "data": ["Merhaba bot!", [], "assistant"]
}

response = requests.post(url, json=data)
result = response.json()
```

### WebSocket Bağlantısı

```javascript
// JavaScript ile real-time sohbet
const ws = new WebSocket('ws://localhost:7861/queue/join');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Bot yanıtı:', data);
};
```

## 📖 Daha Fazla Kaynak

- **Hugging Face Transformers**: <https://huggingface.co/docs/transformers>
- **DialoGPT Modeli**: <https://huggingface.co/microsoft/DialoGPT-medium>
- **Gradio Dökümantasyonu**: <https://gradio.app/docs>
- **PyTorch**: <https://pytorch.org/docs>

---

## 🆘 Destek

Sorunlar için:

1. **Issues** sayfasını kontrol edin
2. **Test dosyalarını** çalıştırın: `python test_chatbot.py`
3. **Log dosyalarını** inceleyin
4. **GitHub Issues** açın

**İyi Sohbetler!** 🤖💬