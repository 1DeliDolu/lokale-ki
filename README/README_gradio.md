# 🤖 Gradio Görsel Açıklayıcı Uygulaması

Bu uygulama Gradio kullanarak görsel yükleme, otomatik başlık atama ve görsel yorumlama işlevlerini sağlar.

## 🚀 Kurulum ve Çalıştırma

### 1. Gerekli Paketleri Yükleyin
```bash
pip install -r requirements_gradio.txt
```

### 2. Uygulamayı Başlatın
```bash
python gradio_image_captioner.py
```

### 3. Tarayıcıda Açın
Uygulama otomatik olarak şu adreste açılacak:
```
http://localhost:7860
```

## ✨ Özellikler

- 📸 **Görsel Yükleme**: Drag & drop veya tıklayarak görsel yükleme
- 🏷️ **Otomatik Başlık**: AI ile otomatik başlık üretimi
- 📝 **Detaylı Açıklama**: Görselin detaylı açıklaması
- ✏️ **Düzenleme**: Üretilen başlık ve açıklamayı düzenleme
- 💾 **Kaydetme**: Görseli başlık ve açıklamayla birlikte kaydetme
- 📱 **Responsive**: Mobil ve masaüstü uyumlu arayüz

## 🔧 Kullanılan Teknolojiler

- **Gradio**: Web arayüzü için
- **Transformers**: BLIP model için
- **Salesforce/blip-image-captioning-base**: Görsel açıklama modeli
- **PyTorch**: Deep learning framework

## 📁 Çıktı Klasörü

Kaydedilen görseller ve açıklamalar `captioned_images/` klasörüne kaydedilir:
- `baslik.jpg`: Görsel dosyası
- `baslik_caption.txt`: Başlık ve açıklama dosyası

## 🎯 Kullanım Senaryoları

- Fotoğraf arşivleme
- Blog içeriği üretimi
- Sosyal medya paylaşımları
- Görme engelliler için alternatif metin
- Veri etiketleme