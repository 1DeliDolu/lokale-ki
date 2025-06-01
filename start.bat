@echo off
REM AI Modülleri Hub - Windows Başlatma Scripti

echo 🚀 AI Modülleri Hub - Başlatılıyor...

REM Sanal ortamın varlığını kontrol et
if not exist "ai_modules_env" (
    echo ❌ Sanal ortam bulunamadı. Önce kurulum yapın:
    echo    install.bat
    pause
    exit /b 1
)

REM Sanal ortamı etkinleştir
echo 🔌 Sanal ortam etkinleştiriliyor...
call ai_modules_env\Scripts\activate.bat

REM Gerekli modüllerin varlığını kontrol et
echo 🧪 Modüller kontrol ediliyor...
python -c "try: import torch, transformers, gradio; print('✅ Tüm modüller hazır!') except ImportError as e: print(f'❌ Eksik modül: {e}'); print('Lütfen kurulum scripti çalıştırın: install.bat'); exit(1)"

if errorlevel 1 (
    pause
    exit /b 1
)

REM Birleşik uygulamayı başlat
echo 🌐 Birleşik AI Hub başlatılıyor...
echo 📸 Görsel Analiz + 💬 ChatGPT Sohbet
echo 🔗 http://localhost:7862
echo.

python run_combined_ai.py
pause