@echo off
REM AI Modülleri Hub - Windows Kurulum Scripti
echo 🚀 AI Modülleri Hub - Kurulum Başlıyor...
echo ================================================

REM Python sürüm kontrolü
echo 🐍 Python sürümü kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Hata: Python bulunamadı. Python 3.8+ yükleyin.
    pause
    exit /b 1
)

REM Sanal ortam oluşturma
echo 📦 Sanal ortam oluşturuluyor...
if not exist "ai_modules_env" (
    python -m venv ai_modules_env
    if errorlevel 1 (
        echo ❌ Sanal ortam oluşturulamadı
        pause
        exit /b 1
    )
    echo ✅ Sanal ortam oluşturuldu: ai_modules_env
) else (
    echo ⚠️  Sanal ortam zaten mevcut
)

REM Sanal ortamı etkinleştirme
echo 🔌 Sanal ortam etkinleştiriliyor...
call ai_modules_env\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Sanal ortam etkinleştirilemedi
    pause
    exit /b 1
)

REM Pip güncelleme
echo ⬆️  Pip güncelleniyor...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ❌ Pip güncellenemedi
    pause
    exit /b 1
)

REM Temel gereksinimler
echo 📚 Temel paketler yükleniyor...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Temel paketler yüklenemedi
    pause
    exit /b 1
)

REM Görsel analiz gereksinimleri
echo 📸 Görsel analiz paketleri yükleniyor...
pip install -r requirements_gradio.txt
if errorlevel 1 (
    echo ❌ Görsel analiz paketleri yüklenemedi
    pause
    exit /b 1
)

REM ChatGPT gereksinimleri
echo 💬 ChatGPT sohbet paketleri yükleniyor...
pip install -r requirements_chatbot.txt
if errorlevel 1 (
    echo ❌ ChatGPT paketleri yüklenemedi
    pause
    exit /b 1
)

REM GPU desteği kontrolü
echo 🎮 GPU desteği kontrol ediliyor...
python -c "import torch; print('CUDA mevcut:', torch.cuda.is_available())" 2>nul

nvidia-smi >nul 2>&1
if not errorlevel 1 (
    echo 🔧 NVIDIA GPU tespit edildi. CUDA destekli PyTorch yüklemek ister misiniz? (y/n)
    set /p response=
    if /i "%response%"=="y" (
        echo ⚡ CUDA destekli PyTorch yükleniyor...
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        if errorlevel 1 (
            echo ❌ CUDA PyTorch yüklenemedi
            pause
            exit /b 1
        )
    )
)

REM Kurulum testi
echo 🧪 Kurulum test ediliyor...
python -c "try: import torch, transformers, gradio, PIL; print('✅ Tüm temel paketler başarıyla yüklendi!'); print(f'PyTorch: {torch.__version__}'); print(f'Transformers: {transformers.__version__}'); print(f'Gradio: {gradio.__version__}') except ImportError as e: print(f'❌ Import hatası: {e}'); exit(1)"
if errorlevel 1 (
    echo ❌ Paket import testi başarısız
    pause
    exit /b 1
)

REM Model önbellek klasörü oluşturma
echo 📁 Model klasörleri oluşturuluyor...
if not exist "models" mkdir models
if not exist "models\huggingface" mkdir models\huggingface
if not exist "models\torch" mkdir models\torch
if not exist "data" mkdir data
if not exist "data\conversations" mkdir data\conversations
if not exist "data\saved_analyses" mkdir data\saved_analyses

REM Kurulum özeti
echo.
echo 🎉 KURULUM TAMAMLANDI!
echo ================================================
echo ✅ Sanal ortam: ai_modules_env
echo ✅ Python paketleri: Tüm gereksinimler yüklendi
echo ✅ Model klasörleri: Oluşturuldu
echo.
echo 🚀 Kullanım:
echo   1. Sanal ortamı etkinleştir: ai_modules_env\Scripts\activate
echo   2. Tüm modüller:            python run_combined_ai.py
echo   3. Sadece görsel analiz:    python run_app.py
echo   4. Sadece ChatGPT sohbet:   python run_chatbot.py
echo.
echo 🌐 Web adresleri:
echo   • Birleşik Hub:     http://localhost:7862
echo   • Görsel Analiz:    http://localhost:7860
echo   • ChatGPT Sohbet:   http://localhost:7861
echo.
echo 💡 İpucu: İlk çalıştırmada modeller otomatik indirilecek (internet bağlantısı gerekli)
echo.
echo İyi kullanımlar! 🤖✨
pause