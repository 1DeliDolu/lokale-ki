#!/bin/bash
# AI Modülleri Hub - Hızlı Başlatma Scripti

echo "🚀 AI Modülleri Hub - Başlatılıyor..."

# Sanal ortamın varlığını kontrol et
if [ ! -d "ai_modules_env" ]; then
    echo "❌ Sanal ortam bulunamadı. Önce kurulum yapın:"
    echo "   ./install.sh"
    exit 1
fi

# Sanal ortamı etkinleştir
echo "🔌 Sanal ortam etkinleştiriliyor..."
source ai_modules_env/bin/activate

# Gerekli modüllerin varlığını kontrol et
echo "🧪 Modüller kontrol ediliyor..."
python -c "
try:
    import torch
    import transformers
    import gradio
    print('✅ Tüm modüller hazır!')
except ImportError as e:
    print(f'❌ Eksik modül: {e}')
    print('Lütfen kurulum scripti çalıştırın: ./install.sh')
    exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Birleşik uygulamayı başlat
echo "🌐 Birleşik AI Hub başlatılıyor..."
echo "📸 Görsel Analiz + 💬 ChatGPT Sohbet"
echo "🔗 http://localhost:7862"
echo ""

python run_combined_ai.py