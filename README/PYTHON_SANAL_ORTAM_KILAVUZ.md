# 🐍 Python Sanal Ortam (Virtual Environment) Kurulum Kılavuzu

Bu kılavuz, Python projeleri için sanal ortam oluşturma ve yönetme işlemlerini detaylı olarak açıklar.

## 🎯 Sanal Ortam Nedir?

Python sanal ortamı (virtual environment), her proje için izole edilmiş Python çalışma alanları oluşturmanızı sağlar. Bu sayede:

- **Bağımlılık Çakışmalarını Önler**: Her proje kendi paket sürümlerini kullanır
- **Sistem Python'unu Korur**: Global Python kurulumunu etkilemez
- **Proje Taşınabilirliği**: Farklı sistemlerde aynı ortamı yeniden oluşturabilir
- **Temiz Geliştirme**: Gereksiz paketlerden arınmış çalışma alanı

## 🚀 Hızlı Başlangıç

### 1. Sanal Ortam Oluşturma

```bash
# Proje dizinine gidin
cd /mnt/d/ki/lokale-ki

# 'ai_modules_env' adında sanal ortam oluşturun
python3 -m venv ai_modules_env
```

### 2. Sanal Ortamı Etkinleştirme

#### Linux/macOS
```bash
# Sanal ortamı etkinleştirin
source ai_modules_env/bin/activate
```

#### Windows (CMD)
```cmd
# Sanal ortamı etkinleştirin
ai_modules_env\Scripts\activate
```

#### Windows (PowerShell)
```powershell
# Sanal ortamı etkinleştirin
ai_modules_env\Scripts\Activate.ps1
```

### 3. Etkinlik Kontrolü

Sanal ortam etkinleştirildiğinde terminal prompt'unda değişiklik göreceksiniz:

```bash
# Öncesi
musta@musta:/mnt/d/ki/lokale-ki$ 

# Sonrası (ai_modules_env etkin)
(ai_modules_env) musta@musta:/mnt/d/ki/lokale-ki$
```

## 📦 Paket Yönetimi

### Paket Kurulumu

```bash
# Sanal ortam etkinken paket kurun
(ai_modules_env) $ pip install gradio
(ai_modules_env) $ pip install torch transformers

# Çoklu paket kurulumu
(ai_modules_env) $ pip install -r requirements.txt
```

### Kurulu Paketleri Listeleme

```bash
# Tüm paketleri listele
(ai_modules_env) $ pip list

# Sadece manuel kurulan paketler
(ai_modules_env) $ pip freeze

# Requirements dosyası oluştur
(ai_modules_env) $ pip freeze > requirements.txt
```

### Paket Güncelleme

```bash
# Tek paket güncelle
(ai_modules_env) $ pip install --upgrade gradio

# Tüm paketleri güncelle
(ai_modules_env) $ pip list --outdated
(ai_modules_env) $ pip install --upgrade package_name
```

## 🔧 Gelişmiş Kullanım

### Farklı Python Sürümü ile Sanal Ortam

```bash
# Python 3.9 ile sanal ortam
python3.9 -m venv ai_modules_env_39

# Python 3.11 ile sanal ortam
python3.11 -m venv ai_modules_env_311

# Belirli sürüm kontrolü
python3 --version
```

### Sanal Ortam Kopyalama

```bash
# Mevcut ortamdan requirements çıkar
(ai_modules_env) $ pip freeze > requirements.txt

# Yeni ortam oluştur
python3 -m venv new_env
source new_env/bin/activate

# Paketleri yeni ortama kur
(new_env) $ pip install -r requirements.txt
```

### Sanal Ortam Silme

```bash
# Önce devre dışı bırak
(ai_modules_env) $ deactivate

# Ortam klasörünü sil
$ rm -rf ai_modules_env
```

## 🎛️ Ortam Yönetimi Komutları

### Temel Komutlar

| Komut | Açıklama |
|-------|----------|
| `python3 -m venv env_name` | Yeni sanal ortam oluştur |
| `source env_name/bin/activate` | Sanal ortamı etkinleştir (Linux/macOS) |
| `env_name\Scripts\activate` | Sanal ortamı etkinleştir (Windows) |
| `deactivate` | Sanal ortamı devre dışı bırak |
| `which python` | Aktif Python yolunu göster |
| `pip list` | Kurulu paketleri listele |

### Durum Kontrolü

```bash
# Hangi Python kullanıldığını kontrol et
(ai_modules_env) $ which python
/mnt/d/ki/lokale-ki/ai_modules_env/bin/python

# Python sürümünü kontrol et
(ai_modules_env) $ python --version
Python 3.11.0

# Pip yolunu kontrol et
(ai_modules_env) $ which pip
/mnt/d/ki/lokale-ki/ai_modules_env/bin/pip
```

## 🏗️ Proje Yapısı Önerisi

```text
lokale-ki/
├── ai_modules_env/             # Sanal ortam (git'e eklenmez)
├── src/                        # Kaynak kod
│   ├── chatbot_module/
│   └── image_analysis/
├── requirements.txt            # Paket listesi
├── requirements-dev.txt        # Geliştirme paketleri
├── .gitignore                 # ai_modules_env/ dahil
├── README.md
└── setup.py
```

### .gitignore Dosyası

```gitignore
# Python sanal ortamları
ai_modules_env/
venv/
env/
.env/

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE ayarları
.vscode/
.idea/

# Sistem dosyaları
.DS_Store
Thumbs.db
```

## 📋 Requirements Dosyası Yönetimi

### Ana Gereksinimler (requirements.txt)

```text
# Web framework
gradio>=4.40.0
fastapi>=0.100.0

# AI/ML
torch>=2.0.0
transformers>=4.35.0
numpy>=1.24.0

# Utilities
python-dotenv>=1.0.0
requests>=2.31.0
```

### Geliştirme Gereksinimleri (requirements-dev.txt)

```text
# Ana gereksinimleri dahil et
-r requirements.txt

# Test araçları
pytest>=7.0.0
pytest-cov>=4.0.0

# Kod kalitesi
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0

# Dökümantasyon
sphinx>=6.0.0
```

### Kurulum Sırası

```bash
# Sanal ortam oluştur ve etkinleştir
python3 -m venv ai_modules_env
source ai_modules_env/bin/activate

# Ana paketleri kur
(ai_modules_env) $ pip install -r requirements.txt

# Geliştirme için ek paketler
(ai_modules_env) $ pip install -r requirements-dev.txt
```

## 🔧 Sorun Giderme

### Yaygın Sorunlar

#### 1. Sanal Ortam Oluşturamama

```bash
# Sorun: venv modülü bulunamadı
# Ubuntu/Debian çözümü:
sudo apt install python3-venv

# CentOS/RHEL çözümü:
sudo yum install python3-venv
```

#### 2. Aktivasyon Sorunu

```bash
# Sorun: "command not found: source"
# Windows Git Bash çözümü:
. ai_modules_env/Scripts/activate

# PowerShell execution policy sorunu:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. Pip Güncelleme Hatası

```bash
# Pip eski sürüm uyarısı
(ai_modules_env) $ python -m pip install --upgrade pip

# SSL sertifika sorunu
(ai_modules_env) $ pip install --trusted-host pypi.org --trusted-host pypi.python.org --upgrade pip
```

#### 4. Paket Çakışması

```bash
# Çözüm: Fresh install
(ai_modules_env) $ pip freeze > temp_requirements.txt
(ai_modules_env) $ deactivate
$ rm -rf ai_modules_env
$ python3 -m venv ai_modules_env
$ source ai_modules_env/bin/activate
(ai_modules_env) $ pip install -r temp_requirements.txt
```

## 🛠️ İleri Seviye İpuçları

### 1. Otomatik Aktivasyon

`.bashrc` veya `.zshrc` dosyasına ekleyin:

```bash
# Proje dizinine girerken otomatik aktivasyon
cd() {
    builtin cd "$@"
    if [[ -f "./ai_modules_env/bin/activate" ]]; then
        source ./ai_modules_env/bin/activate
    fi
}
```

### 2. Ortam Değişkenleri

`.env` dosyası oluşturun:

```bash
# .env dosyası
PYTHONPATH=/mnt/d/ki/lokale-ki/src
DEBUG=True
MODEL_CACHE_DIR=./models
```

Python'da kullanım:

```python
from dotenv import load_dotenv
import os

load_dotenv()
debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
```

### 3. Conda Alternatifi

```bash
# Miniconda kurulu ise
conda create -n ai_modules_env python=3.11
conda activate ai_modules_env
conda install pytorch transformers -c pytorch
```

## 🚀 Proje İçin Özel Kurulum

### AI Modülleri Hub için

```bash
# 1. Sanal ortam oluştur
cd /mnt/d/ki/lokale-ki
python3 -m venv ai_modules_env

# 2. Etkinleştir
source ai_modules_env/bin/activate

# 3. Gerekli paketleri kur
(ai_modules_env) $ pip install --upgrade pip
(ai_modules_env) $ pip install -r requirements.txt
(ai_modules_env) $ pip install -r requirements_gradio.txt
(ai_modules_env) $ pip install -r requirements_chatbot.txt

# 4. GPU desteği (opsiyonel)
(ai_modules_env) $ pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 5. Test kurulumu
(ai_modules_env) $ python test_module.py
(ai_modules_env) $ python test_chatbot.py

# 6. Uygulamayı çalıştır
(ai_modules_env) $ python run_combined_ai.py
```

### Hızlı Başlatma Scripti

`activate_env.sh` dosyası oluşturun:

```bash
#!/bin/bash
# activate_env.sh

echo "🐍 AI Modülleri Hub - Sanal Ortam Başlatılıyor..."

# Sanal ortamı etkinleştir
source ai_modules_env/bin/activate

# Durum bilgisi göster
echo "✅ Sanal ortam etkinleştirildi: $(which python)"
echo "📦 Python sürümü: $(python --version)"
echo "🚀 Kullanım: python run_combined_ai.py"
echo ""

# Terminal başlat
exec bash
```

Kullanım:

```bash
chmod +x activate_env.sh
./activate_env.sh
```

## 📚 Referanslar

- **Python venv**: <https://docs.python.org/3/tutorial/venv.html>
- **Pip kullanım kılavuzu**: <https://pip.pypa.io/en/stable/user_guide/>
- **Virtual Environment Best Practices**: <https://realpython.com/python-virtual-environments/>

---

## 🎯 Özet

```bash
# Temel işlem akışı
cd /mnt/d/ki/lokale-ki
python3 -m venv ai_modules_env
source ai_modules_env/bin/activate
pip install -r requirements.txt
python run_combined_ai.py
deactivate
```

**Başarılı sanal ortam yönetimi dileriz!** 🐍✨