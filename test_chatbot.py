"""
ChatGPT Benzeri Sohbet Botu Test ve Örnek Kullanım
"""

from chatbot_module import (
    ChatGPTLikeBot, 
    ConversationManager,
    ModelPresets,
    quick_chat,
    create_conversation
)
import os

def test_basic_chat():
    """
    Temel sohbet testi
    """
    print("🤖 Temel Sohbet Testi")
    print("=" * 40)
    
    try:
        # Hızlı sohbet
        response = quick_chat("Merhaba! Nasılsın?")
        print(f"Kullanıcı: Merhaba! Nasılsın?")
        print(f"Bot: {response}")
        
        # Başka bir mesaj
        response = quick_chat("Python hakkında bilgi verebilir misin?")
        print(f"\nKullanıcı: Python hakkında bilgi verebilir misin?")
        print(f"Bot: {response}")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

def test_different_bot_types():
    """
    Farklı bot türleri testi
    """
    print("\n🎭 Farklı Bot Türleri Testi")
    print("=" * 40)
    
    try:
        # Yardımcı asistan
        assistant_bot = ChatGPTLikeBot(ModelPresets.helpful_assistant())
        response = assistant_bot.chat("Yapay zeka nedir?")
        print(f"🤝 Asistan: {response}")
        
        # Yaratıcı yazar (eğer model yüklenmişse)
        # creative_bot = ChatGPTLikeBot(ModelPresets.creative_writer())
        # response = creative_bot.chat("Kısa bir hikaye yaz")
        # print(f"🎨 Yaratıcı: {response}")
        
        # Teknik uzman
        # tech_bot = ChatGPTLikeBot(ModelPresets.technical_expert())
        # response = tech_bot.chat("HTTP protokolü nasıl çalışır?")
        # print(f"⚙️ Teknisyen: {response}")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

def test_conversation_history():
    """
    Konuşma geçmişi testi
    """
    print("\n📚 Konuşma Geçmişi Testi")
    print("=" * 40)
    
    try:
        bot = ChatGPTLikeBot()
        
        # Yeni konuşma başlat
        conv_id = bot.start_new_conversation("Test Konuşması")
        print(f"✅ Yeni konuşma oluşturuldu: {conv_id}")
        
        # Konuşma yap
        messages = [
            "Merhaba!",
            "Adın ne?",
            "Hangi konularda yardımcı olabilirsin?"
        ]
        
        for msg in messages:
            response = bot.chat(msg, conv_id)
            print(f"👤 Kullanıcı: {msg}")
            print(f"🤖 Bot: {response}")
            print()
        
        # Konuşma listesini göster
        conversations = bot.get_conversation_list()
        print(f"📋 Toplam konuşma sayısı: {len(conversations)}")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

def test_conversation_manager():
    """
    Konuşma yöneticisi testi
    """
    print("\n👥 Konuşma Yöneticisi Testi")
    print("=" * 40)
    
    try:
        manager = ConversationManager()
        
        # Farklı botlar oluştur
        manager.create_bot("bot1", ModelPresets.conversational_model())
        manager.create_bot("bot2", ModelPresets.helpful_assistant())
        
        # Bot listesi
        bots = manager.list_bots()
        print(f"📋 Mevcut botlar: {bots}")
        
        # Bot1 ile sohbet
        response1 = manager.chat_with_bot("bot1", "Merhaba bot1!")
        print(f"🤖 Bot1: {response1}")
        
        # Bot2 ile sohbet
        response2 = manager.chat_with_bot("bot2", "Merhaba bot2!")
        print(f"🤖 Bot2: {response2}")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

def test_model_info():
    """
    Model bilgileri testi
    """
    print("\n📊 Model Bilgileri Testi")
    print("=" * 40)
    
    try:
        bot = ChatGPTLikeBot()
        info = bot.get_model_info()
        
        print(f"🤖 Model: {info['model_name']}")
        print(f"📱 Device: {info['device']}")
        print(f"🔧 CUDA: {'✅' if info['cuda_available'] else '❌'}")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

def interactive_chat():
    """
    İnteraktif sohbet testi
    """
    print("\n💬 İnteraktif Sohbet")
    print("=" * 40)
    print("'quit' yazarak çıkabilirsiniz.")
    print()
    
    try:
        bot = ChatGPTLikeBot()
        
        while True:
            user_input = input("👤 Siz: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'çık', 'bye']:
                print("👋 Görüşürüz!")
                break
            
            if not user_input:
                continue
            
            response = bot.chat(user_input)
            print(f"🤖 Bot: {response}")
            print()
            
    except KeyboardInterrupt:
        print("\n👋 Sohbet sonlandırıldı!")
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

def main():
    """
    Tüm testleri çalıştır
    """
    print("🧪 ChatGPT Benzeri Sohbet Botu Testleri")
    print("=" * 60)
    
    try:
        test_basic_chat()
        test_different_bot_types()
        test_conversation_history()
        test_conversation_manager()
        test_model_info()
        
        print("\n" + "=" * 60)
        print("✅ Tüm testler tamamlandı!")
        print("💬 İnteraktif sohbet başlatmak ister misiniz? (y/n)")
        
        choice = input().lower().strip()
        if choice in ['y', 'yes', 'evet', 'e']:
            interactive_chat()
        
    except KeyboardInterrupt:
        print("\n⏹️ Testler durduruldu")
    except Exception as e:
        print(f"\n❌ Test hatası: {str(e)}")

if __name__ == "__main__":
    main()