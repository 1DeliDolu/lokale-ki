# ⚡ Hızlı Kurulum Talimatları

Bu dosya, AI Modülleri Hub'ın hızlı kurulumu için adım adım talimatlar içerir.

## 🚀 Otomatik Kurulum (Önerilen)

### Linux/macOS
```bash
cd /mnt/d/ki/lokale-ki
chmod +x install.sh
./install.sh
```

### Windows
```cmd
cd d:\ki\lokale-ki
install.bat
```

## 🔧 Manuel Kurulum

### 1. Sanal Ortam Oluşturma
```bash
# Linux/macOS
cd /mnt/d/ki/lokale-ki
python3 -m venv ai_modules_env
source ai_modules_env/bin/activate

# Windows
cd d:\ki\lokale-ki
python -m venv ai_modules_env
ai_modules_env\Scripts\activate
```

### 2. Gereksinimleri Yükleme
```bash
# Pip güncelle
python -m pip install --upgrade pip

# Ana paketler
pip install -r requirements.txt

# Görsel analiz paketleri
pip install -r requirements_gradio.txt

# ChatGPT sohbet paketleri
pip install -r requirements_chatbot.txt
```

### 3. GPU Desteği (Opsiyonel)
```bash
# NVIDIA GPU için CUDA destekli PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Apple Silicon (M1/M2) için
pip install torch torchvision torchaudio
```

## 🧪 Kurulum Testi

```bash
# Modül testleri
python test_module.py
python test_chatbot.py

# Import testi
python -c "import torch, transformers, gradio; print('✅ Kurulum başarılı!')"
```

## 🚀 Uygulamaları Çalıştırma

```bash
# Tüm modüller birlikte (önerilen)
python run_combined_ai.py

# Sadece görsel analiz
python run_app.py

# Sadece ChatGPT sohbet
python run_chatbot.py
```

## 🌐 Web Adresleri

- **Birleşik Hub**: http://localhost:7862
- **Görsel Analiz**: http://localhost:7860
- **ChatGPT Sohbet**: http://localhost:7861

## 🔧 Sorun Giderme

### Requirements Dosyası Bulunamadı
```bash
# Tüm requirements dosyalarının mevcut olduğunu kontrol edin
ls -la requirements*.txt

# Eksikse bu komutu çalıştırın
git pull origin main
```

### Python/Pip Hatası
```bash
# Python sürümü (3.8+ gerekli)
python --version

# Pip yeniden kurulum
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### CUDA/GPU Sorunu
```bash
# CPU-only PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# CUDA kontrolü
python -c "import torch; print(torch.cuda.is_available())"
```

### Port Çakışması
```bash
# Farklı port kullan
python run_combined_ai.py --port 7863

# Çalışan işlemi durdur
lsof -ti:7862 | xargs kill  # Linux/macOS
netstat -ano | findstr :7862  # Windows
```

## 📋 Dosya Listesi

Kurulum sonrası bu dosyalar mevcut olmalı:

```text
lokale-ki/
├── requirements.txt           ✅ Ana gereksinimler
├── requirements_gradio.txt    ✅ Görsel analiz
├── requirements_chatbot.txt   ✅ ChatGPT sohbet
├── install.sh                ✅ Linux/macOS kurulum
├── install.bat               ✅ Windows kurulum
├── ai_modules_env/           ✅ Sanal ortam
├── run_combined_ai.py        ✅ Birleşik uygulama
├── run_app.py               ✅ Görsel analiz app
├── run_chatbot.py           ✅ Sohbet app
└── test_*.py                ✅ Test dosyaları
```

---

**Hızlı Başlangıç**: `./install.sh` (Linux/macOS) veya `install.bat` (Windows)