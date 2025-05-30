#!/usr/bin/env python3
"""
ChatGPT Benzeri Sohbet Botu - Ana Başlatıcı
Gradio arayüzünü başlatmak için bu dosyayı çalıştırın.
"""

from chatbot_gradio_interface import launch_chatbot_app
import sys

def main():
    """
    Sohbet botu uygulaması başlatıcısı
    """
    print("🤖 ChatGPT Benzeri Sohbet Botu")
    print("=" * 50)
    print("📡 Gradio arayüzü başlatılıyor...")
    print("🌐 Tarayıcınızda http://localhost:7861 adresini açın")
    print("⏹️  Durdurmak için Ctrl+C tuşlarına basın")
    print("🤖 Açık kaynak LLM'ler ile ChatGPT deneyimi!")
    print("-" * 50)
    
    try:
        # Sohbet botu uygulamasını başlat
        launch_chatbot_app(
            server_name="0.0.0.0",
            server_port=7861,
            share=False  # True yaparsanız public link alır
        )
    except KeyboardInterrupt:
        print("\n✅ Sohbet botu kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()