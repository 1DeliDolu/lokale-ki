#!/usr/bin/env python3
"""
AI Görsel Açıklayıcı - Ana Başlatıcı
Gradio arayüzünü başlatmak için bu dosyayı çalıştırın.
"""

from gradio_interface import launch_gradio_app
import sys

def main():
    """
    Ana uygulama başlatıcısı
    """
    print("🤖 AI Görsel Açıklayıcı")
    print("=" * 40)
    print("📡 Gradio arayüzü başlatılıyor...")
    print("🌐 Tarayıcınızda http://localhost:7860 adresini açın")
    print("⏹️  Durdurmak için Ctrl+C tuşlarına basın")
    print("-" * 40)
    
    try:
        # Gradio uygulamasını başlat
        launch_gradio_app(
            server_name="0.0.0.0",
            server_port=7860,
            share=False  # True yaparsanız public link alır
        )
    except KeyboardInterrupt:
        print("\n✅ Uygulama kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()