#!/bin/bash
# AI Modülleri Hub - Otomatik Kurulum Scripti

echo "🚀 AI Modülleri Hub - Kurulum Başlıyor..."
echo "=" * 50

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Hata kontrolü fonksiyonu
check_error() {
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Hata: $1${NC}"
        exit 1
    fi
}

# Python sürüm kontrolü
echo -e "${BLUE}🐍 Python sürümü kontrol ediliyor...${NC}"
python3 --version
check_error "Python3 bulunamadı. Python 3.8+ yükleyin."

# Sanal ortam oluşturma
echo -e "${BLUE}📦 Sanal ortam oluşturuluyor...${NC}"
if [ ! -d "ai_modules_env" ]; then
    python3 -m venv ai_modules_env
    check_error "Sanal ortam oluşturulamadı"
    echo -e "${GREEN}✅ Sanal ortam oluşturuldu: ai_modules_env${NC}"
else
    echo -e "${YELLOW}⚠️  Sanal ortam zaten mevcut${NC}"
fi

# Sanal ortamı etkinleştirme
echo -e "${BLUE}🔌 Sanal ortam etkinleştiriliyor...${NC}"
source ai_modules_env/bin/activate
check_error "Sanal ortam etkinleştirilemedi"

# Pip güncelleme
echo -e "${BLUE}⬆️  Pip güncelleniyor...${NC}"
python -m pip install --upgrade pip
check_error "Pip güncellenemedi"

# Temel gereksinimler
echo -e "${BLUE}📚 Temel paketler yükleniyor...${NC}"
pip install -r requirements.txt
check_error "Temel paketler yüklenemedi"

# Görsel analiz gereksinimleri
echo -e "${BLUE}📸 Görsel analiz paketleri yükleniyor...${NC}"
pip install -r requirements_gradio.txt
check_error "Görsel analiz paketleri yüklenemedi"

# ChatGPT gereksinimleri
echo -e "${BLUE}💬 ChatGPT sohbet paketleri yükleniyor...${NC}"
pip install -r requirements_chatbot.txt
check_error "ChatGPT paketleri yüklenemedi"

# GPU desteği kontrolü (opsiyonel)
echo -e "${BLUE}🎮 GPU desteği kontrol ediliyor...${NC}"
python -c "import torch; print('CUDA mevcut:', torch.cuda.is_available())" 2>/dev/null

if command -v nvidia-smi &> /dev/null; then
    echo -e "${YELLOW}🔧 NVIDIA GPU tespit edildi. CUDA destekli PyTorch yüklemek ister misiniz? (y/n)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${BLUE}⚡ CUDA destekli PyTorch yükleniyor...${NC}"
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        check_error "CUDA PyTorch yüklenemedi"
    fi
fi

# Kurulum testi
echo -e "${BLUE}🧪 Kurulum test ediliyor...${NC}"
python -c "
try:
    import torch
    import transformers
    import gradio
    import PIL
    print('✅ Tüm temel paketler başarıyla yüklendi!')
    print(f'PyTorch: {torch.__version__}')
    print(f'Transformers: {transformers.__version__}')
    print(f'Gradio: {gradio.__version__}')
except ImportError as e:
    print(f'❌ Import hatası: {e}')
    exit(1)
"
check_error "Paket import testi başarısız"

# Model önbellek klasörü oluşturma
echo -e "${BLUE}📁 Model klasörleri oluşturuluyor...${NC}"
mkdir -p models/huggingface
mkdir -p models/torch
mkdir -p data/conversations
mkdir -p data/saved_analyses

# Kurulum özeti
echo ""
echo -e "${GREEN}🎉 KURULUM TAMAMLANDI!${NC}"
echo "=" * 50
echo -e "${GREEN}✅ Sanal ortam:${NC} ai_modules_env"
echo -e "${GREEN}✅ Python paketleri:${NC} Tüm gereksinimler yüklendi"
echo -e "${GREEN}✅ Model klasörleri:${NC} Oluşturuldu"
echo ""
echo -e "${BLUE}🚀 Kullanım:${NC}"
echo "  1. Sanal ortamı etkinleştir: source ai_modules_env/bin/activate"
echo "  2. Tüm modüller:            python run_combined_ai.py"
echo "  3. Sadece görsel analiz:    python run_app.py"
echo "  4. Sadece ChatGPT sohbet:   python run_chatbot.py"
echo ""
echo -e "${BLUE}🌐 Web adresleri:${NC}"
echo "  • Birleşik Hub:     http://localhost:7862"
echo "  • Görsel Analiz:    http://localhost:7860"
echo "  • ChatGPT Sohbet:   http://localhost:7861"
echo ""
echo -e "${YELLOW}💡 İpucu:${NC} İlk çalıştırmada modeller otomatik indirilecek (internet bağlantısı gerekli)"
echo ""
echo -e "${GREEN}İyi kullanımlar! 🤖✨${NC}"