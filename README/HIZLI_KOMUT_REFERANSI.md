# 🚀 Python Sanal Ortam - Hızlı Komut Referansı

Bu dosya, Python sanal ortam yönetimi için en çok kullanılan komutların hızlı referansıdır.

## ⚡ Temel Komutlar

### Sanal Ortam Oluşturma

```bash
# Yeni sanal ortam oluştur
python3 -m venv ai_modules_env

# Belirli Python sürümü ile
python3.11 -m venv ai_modules_env_311
```

### Etkinleştirme/Devre Dışı Bırakma

```bash
# Linux/macOS - Etkinleştir
source ai_modules_env/bin/activate

# Windows CMD - Etkinleştir  
ai_modules_env\Scripts\activate

# Windows PowerShell - Etkinleştir
ai_modules_env\Scripts\Activate.ps1

# Devre dışı bırak (tüm platformlar)
deactivate
```

### Paket Yönetimi

```bash
# Paket kur
pip install package_name

# Requirements dosyasından kur
pip install -r requirements.txt

# Paket listele
pip list

# Requirements dosyası oluştur
pip freeze > requirements.txt

# Paket güncelle
pip install --upgrade package_name

# Pip güncelle
python -m pip install --upgrade pip
```

## 🔍 Durum Kontrolü

```bash
# Aktif Python yolu
which python

# Python sürümü
python --version

# Pip yolu
which pip

# Sanal ortam durumu (prompt değişikliği)
# (ai_modules_env) user@host:~/project$
```

## 📦 AI Modülleri Hub İçin Özel Kurulum

```bash
# 1. Proje dizinine git
cd /mnt/d/ki/lokale-ki

# 2. Sanal ortam oluştur
python3 -m venv ai_modules_env

# 3. Etkinleştir
source ai_modules_env/bin/activate

# 4. Pip güncelle
pip install --upgrade pip

# 5. Temel paketleri kur
pip install -r requirements.txt

# 6. Görsel analiz paketleri
pip install -r requirements_gradio.txt

# 7. ChatGPT sohbet paketleri
pip install -r requirements_chatbot.txt

# 8. GPU desteği (opsiyonel)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 9. Test kurulumu
python test_module.py
python test_chatbot.py

# 10. Uygulamayı çalıştır
python run_combined_ai.py
```

## 🛠️ Sorun Giderme Komutları

```bash
# Python3-venv kurulumu (Ubuntu/Debian)
sudo apt install python3-venv

# Execution policy (Windows PowerShell)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# SSL problemi için güvenilir host
pip install --trusted-host pypi.org --trusted-host pypi.python.org package_name

# Cache temizleme
pip cache purge

# Ortam yeniden oluşturma
rm -rf ai_modules_env
python3 -m venv ai_modules_env
source ai_modules_env/bin/activate
pip install -r requirements.txt
```

## 📋 Yaygın Dosya Yapısı

```text
lokale-ki/
├── ai_modules_env/        # Sanal ortam (git'e eklenmez)
├── requirements.txt       # Ana paketler
├── requirements_gradio.txt    # Görsel analiz
├── requirements_chatbot.txt   # Sohbet botu
├── .env                   # Ortam değişkenleri
├── .gitignore            # ai_modules_env/ dahil
└── activate_env.sh       # Hızlı başlatma scripti
```

## 🎯 Günlük Kullanım Akışı

```bash
# Sabah - Projeye başlarken
cd /mnt/d/ki/lokale-ki
source ai_modules_env/bin/activate
python run_combined_ai.py

# Geliştirme sırasında
pip install new_package
pip freeze > requirements.txt

# Akşam - İşi bitirirken
deactivate
```

## 💡 Pro İpuçları

```bash
# Terminal başlığında ortam adını göster
export PS1="($(basename $VIRTUAL_ENV)) $PS1"

# Otomatik aktivasyon için alias
alias activate_ai="cd /mnt/d/ki/lokale-ki && source ai_modules_env/bin/activate"

# Hızlı test komutu
alias test_ai="python test_module.py && python test_chatbot.py"

# Hızlı başlatma
alias run_ai="python run_combined_ai.py"
```

---

**Hızlı Başlangıç:** `python3 -m venv ai_modules_env && source ai_modules_env/bin/activate && pip install -r requirements.txt`