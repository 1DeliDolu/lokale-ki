# 🚀 AI Modülleri Hub - Kurulum Kılavuzu

Bu kılavuz, AI Modülleri Hub'ın sisteminizde kurulumu ve yapılandırılması için adım adım talimatlar içerir.

## 📋 Sistem Gereksinimleri

### Minimum Gereksinimler

- **İşletim Sistemi**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 veya üzeri (3.11 önerilir)
- **RAM**: 8GB (16GB önerilir)
- **Disk Alanı**: 5GB boş alan
- **İnternet**: Model indirme için

### Önerilen Gereksinimler

- **GPU**: NVIDIA GPU (CUDA destekli) - isteğe bağlı
- **RAM**: 16GB veya üzeri
- **CPU**: 4 çekirdek veya üzeri
- **Disk**: SSD tercih edilir

## 🔧 Kurulum Adımları

### 1. Python Kurulumu

#### Windows

```bash
# Python 3.11 indirin ve kurun
# https://python.org/downloads/

# Kurulumu doğrulayın
python --version
pip --version
```

#### macOS

```bash
# Homebrew ile
brew install python@3.11

# Veya resmi installer
# https://python.org/downloads/
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3.11-pip
```

### 2. Proje Klonlama

```bash
# Git ile klonlayın
git clone <repository-url>
cd lokale-ki

# Veya ZIP dosyasını indirip açın
```

### 3. Virtual Environment Oluşturma

```bash
# Virtual environment oluştur
python -m venv ai_modules_env

# Aktif et (Windows)
ai_modules_env\Scripts\activate

# Aktif et (macOS/Linux)
source ai_modules_env/bin/activate
```

### 4. Gerekli Paketleri Yükleme

#### Temel Kurulum

```bash
# Pip güncelle
python -m pip install --upgrade pip

# Temel gereksinimler
pip install -r requirements.txt
```

#### Modül Bazında Kurulum

```bash
# Sadece Görsel Analiz için
pip install -r requirements_gradio.txt

# Sadece ChatGPT Sohbet için
pip install -r requirements_chatbot.txt

# Tüm modüller için (önerilen)
pip install -r requirements.txt
pip install -r requirements_gradio.txt
pip install -r requirements_chatbot.txt
```

### 5. GPU Desteği (İsteğe Bağlı)

#### NVIDIA GPU için

```bash
# CUDA destekli PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA kurulumunu doğrula
python -c "import torch; print(torch.cuda.is_available())"
```

#### Apple Silicon (M1/M2) için

```bash
# Metal Performance Shaders desteği
pip install torch torchvision torchaudio
```

## 🎯 İlk Çalıştırma

### 1. Test Kurulumu

```bash
# Modülleri test et
python test_module.py        # Görsel analiz testi
python test_chatbot.py       # Sohbet botu testi
```

### 2. Uygulamaları Başlatma

```bash
# Tüm modüller birlikte (önerilen)
python run_combined_ai.py

# Sadece görsel analiz
python run_app.py

# Sadece sohbet botu
python run_chatbot.py
```

### 3. Web Arayüzüne Erişim

- **Birleşik Hub**: <http://localhost:7862>
- **Görsel Analiz**: <http://localhost:7860>
- **ChatGPT Sohbet**: <http://localhost:7861>

## 🔧 Konfigürasyon

### Ortam Değişkenleri

`.env` dosyası oluşturun:

```bash
# Model ayarları
TORCH_HOME=./models
HF_HOME=./huggingface
TRANSFORMERS_CACHE=./cache

# Server ayarları
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7862

# Güvenlik (production için)
GRADIO_AUTH=username:password
```

### Ayar Dosyaları

#### Görsel Analiz Ayarları

`image_config.json` oluşturun:

```json
{
  "model_name": "Salesforce/blip-image-captioning-base",
  "device": "auto",
  "max_image_size": [1024, 1024],
  "output_quality": 85,
  "save_metadata": true
}
```

#### ChatGPT Ayarları

`chatbot_config.json` oluşturun:

```json
{
  "model_name": "microsoft/DialoGPT-medium",
  "temperature": 0.8,
  "max_new_tokens": 150,
  "conversation_history_limit": 10,
  "system_message": "Sen yardımsever bir AI asistanısın."
}
```

## 🐳 Docker Kurulumu

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

# Sistem paketleri
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Gereksinimler
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements_gradio.txt && \
    pip install --no-cache-dir -r requirements_chatbot.txt

# Uygulama dosyaları
COPY . .

# Port açma
EXPOSE 7862

# Başlatma komutu
CMD ["python", "run_combined_ai.py"]
```

### 2. Docker Compose

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  ai-modules:
    build: .
    ports:
      - "7862:7862"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    environment:
      - TORCH_HOME=/app/models
      - HF_HOME=/app/models/huggingface
    restart: unless-stopped
```

### 3. Çalıştırma

```bash
# Build ve çalıştır
docker-compose up --build

# Arka planda çalıştır
docker-compose up -d
```

## 🔧 Sorun Giderme

### Yaygın Kurulum Sorunları

#### 1. Python Sürüm Hatası

```bash
# Sorun: Python 3.7 veya daha eski
# Çözüm: Python 3.8+ yükleyin

python --version  # 3.8+ olmalı
```

#### 2. Pip Hatası

```bash
# Sorun: pip bulunamadı
# Çözüm: pip yeniden yükleyin

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

#### 3. PyTorch CUDA Hatası

```bash
# Sorun: CUDA uyumsuzluğu
# Çözüm: CPU sürümü kullanın

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### 4. Model İndirme Hatası

```bash
# Sorun: HuggingFace erişim hatası
# Çözüm: Manuel cache temizleme

rm -rf ~/.cache/huggingface/
pip install --upgrade transformers
```

### Port Çakışması

```bash
# Port 7862 kullanımda
# Farklı port kullan
python run_combined_ai.py --port 7863

# Veya çalışan süreci durdur
netstat -ano | findstr :7862  # Windows
lsof -ti:7862 | xargs kill    # macOS/Linux
```

### Bellek Sorunları

```bash
# RAM yetersiz
# Küçük model kullan
export MODEL_SIZE=small
python run_combined_ai.py
```

## 📊 Performans Optimizasyonu

### CPU Optimizasyonu

```python
# config.py içinde
import torch

# CPU çekirdek sayısını ayarla
torch.set_num_threads(4)

# Model konfigürasyonu
config = {
    "device": "cpu",
    "model_size": "small",
    "batch_size": 1
}
```

### GPU Optimizasyonu

```python
# GPU bellek ayarları
import torch

if torch.cuda.is_available():
    # Bellek temizleme
    torch.cuda.empty_cache()
    
    # Bellek kullanım limiti
    torch.cuda.set_per_process_memory_fraction(0.8)
```

### Disk Alanı Optimizasyonu

```bash
# Model cache temizleme
rm -rf ~/.cache/huggingface/transformers/
rm -rf ~/.cache/torch/hub/

# Log dosyası temizleme
find . -name "*.log" -delete
```

## 🚀 Production Deployment

### 1. Nginx Proxy

`nginx.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:7862;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Systemd Service

`/etc/systemd/system/ai-modules.service`:

```ini
[Unit]
Description=AI Modules Hub
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ai-modules
ExecStart=/opt/ai-modules/ai_modules_env/bin/python run_combined_ai.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. SSL Sertifikası

```bash
# Let's Encrypt ile
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 📦 Güncelleme

### Kod Güncelleme

```bash
# Git pull
git pull origin main

# Gereksinimleri güncelle
pip install -r requirements.txt --upgrade
```

### Model Güncelleme

```bash
# Cache temizle
rm -rf ~/.cache/huggingface/

# Modelleri yeniden indir
python -c "from transformers import AutoModel; AutoModel.from_pretrained('microsoft/DialoGPT-medium')"
```

## 🔒 Güvenlik

### Temel Güvenlik

```python
# Gradio auth ekle
import gradio as gr

interface.launch(
    auth=("username", "password"),
    ssl_keyfile="path/to/key.pem",
    ssl_certfile="path/to/cert.pem"
)
```

### Firewall Ayarları

```bash
# Sadece gerekli portları aç
sudo ufw allow 80
sudo ufw allow 443
sudo ufw deny 7862  # Direct access engelle
```

## 📚 Ek Kaynaklar

- **Python Kurulum**: <https://python.org/downloads/>
- **PyTorch Kurulum**: <https://pytorch.org/get-started/>
- **CUDA Toolkit**: <https://developer.nvidia.com/cuda-toolkit>
- **Docker**: <https://docs.docker.com/get-docker/>

---

## 🆘 Destek

Kurulum sorunları için:

1. **Dokümanları** tekrar okuyun
2. **Test komutlarını** çalıştırın
3. **Log dosyalarını** kontrol edin
4. **GitHub Issues** açın

**Başarılı kurulum dileriz!** 🚀✨