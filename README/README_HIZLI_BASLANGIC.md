# 🤖 AI Modülleri Hub - Hızlı Başlangıç

Bu README, AI Modülleri Hub'ın hızlı kurulumu ve kullanımı için temel talimatları içerir.

## ⚡ Otomatik Kurulum (Önerilen)

### Linux/macOS
```bash
cd /mnt/d/ki/lokale-ki
chmod +x install.sh start.sh
./install.sh
./start.sh
```

### Windows
```cmd
cd d:\ki\lokale-ki
install.bat
start.bat
```

## 🐍 Sanal Ortam: `ai_modules_env`

Bu proje `ai_modules_env` adlı Python sanal ortamını kullanır.

### Manuel Aktivasyon

**Linux/macOS:**
```bash
source ai_modules_env/bin/activate
```

**Windows:**
```cmd
ai_modules_env\Scripts\activate
```

### Devre Dışı Bırakma
```bash
deactivate
```

## 📦 Gereksinimler

- **Python 3.8+**
- **pip** (Python paket yöneticisi)
- **İnternet bağlantısı** (model indirimi için)
- **Minimum 4GB RAM** (AI modelleri için)

## 🚀 Kullanım

### Tüm Modüller (Birleşik Hub)
```bash
python run_combined_ai.py
# 🌐 http://localhost:7862
```

### Sadece Görsel Analiz
```bash
python run_app.py
# 📸 http://localhost:7860
```

### Sadece ChatGPT Sohbet
```bash
python run_chatbot.py
# 💬 http://localhost:7861
```

## 🔧 Sorun Giderme

### `requirements.txt` Bulunamadı
Gerekli requirements dosyaları mevcuttur:
- `requirements.txt` - Ana gereksinimler
- `requirements_gradio.txt` - Görsel analiz
- `requirements_chatbot.txt` - Sohbet botu

### Sanal Ortam Bulunamadı
```bash
python3 -m venv ai_modules_env
source ai_modules_env/bin/activate  # Linux/macOS
# ai_modules_env\Scripts\activate   # Windows
```

### Port Çakışması
```bash
# Farklı port kullan
python run_combined_ai.py --port 7863
```

## 📚 Dökümantasyon

- **[Python Sanal Ortam Kılavuzu](PYTHON_SANAL_ORTAM_KILAVUZ.md)** - Detaylı sanal ortam rehberi
- **[Hızlı Komut Referansı](HIZLI_KOMUT_REFERANSI.md)** - En çok kullanılan komutlar
- **[Hızlı Kurulum](HIZLI_KURULUM.md)** - Kurulum talimatları
- **[ChatGPT Kılavuzu](CHATBOT_KILAVUZ.md)** - Sohbet botu kullanımı
- **[Görsel Analiz Kılavuzu](GORSEL_ANALIZ_KILAVUZ.md)** - Görsel analiz modülü

## 🎯 Özellikler

### 📸 Görsel Analiz Modülü
- **BLIP modeli** ile görsel açıklama
- **Gradio web arayüzü**
- **Çoklu format desteği** (JPEG, PNG, WebP)
- **Türkçe açıklamalar**

### 💬 ChatGPT Benzeri Sohbet
- **Açık kaynak LLM'ler**
- **Gradio sohbet arayüzü**
- **Konuşma geçmişi**
- **Özelleştirilebilir parametreler**

## 🌟 Hızlı Komutlar

```bash
# Kurulum
./install.sh  # Linux/macOS
install.bat   # Windows

# Başlatma
./start.sh    # Linux/macOS
start.bat     # Windows

# Sanal ortam
source ai_modules_env/bin/activate  # Etkinleştir
deactivate                          # Devre dışı

# Uygulama
python run_combined_ai.py          # Tüm modüller
python run_app.py                  # Sadece görsel
python run_chatbot.py              # Sadece sohbet
```

---

**İyi kullanımlar!** 🤖✨

*Daha fazla bilgi için dökümantasyon dosyalarını inceleyin.*