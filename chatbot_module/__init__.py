"""
ChatGPT Benzeri Sohbet Botu Modülü

Bu modül, açık kaynak LLM'ler kullanarak ChatGPT benzeri bir sohbet botu oluşturur.
Hugging Face transformers kütüphanesi ile entegre çalışır.

Kullanım:
    from chatbot_module import ChatGPTLikeBot
    
    bot = ChatGPTLikeBot()
    response = bot.chat("Merhaba!")
"""

from .chatbot import ChatGPTLikeBot, ConversationManager
from .config import ChatbotConfig, ModelPresets
from .utils import ChatUtils, ConversationHistory
from .exceptions import ChatbotError, ModelLoadError

__version__ = "1.0.0"
__author__ = "AI Development Team"
__email__ = "mustafa.ozdemir1408@gmail.com"

# Ana sınıfları dışa aktar
__all__ = [
    'ChatGPTLikeBot',
    'ConversationManager',
    'ChatbotConfig',
    'ModelPresets',
    'ChatUtils',
    'ConversationHistory',
    'ChatbotError',
    'ModelLoadError'
]

# Modül seviyesinde kolaylık fonksiyonları
def quick_chat(message: str, model_name: str = None) -> str:
    """
    Hızlı sohbet fonksiyonu
    
    Args:
        message (str): Kullanıcı mesajı
        model_name (str, optional): Model adı
    
    Returns:
        str: Bot yanıtı
    """
    bot = ChatGPTLikeBot(model_name=model_name)
    return bot.chat(message)

def create_conversation() -> ConversationManager:
    """
    Yeni konuşma oluştur
    
    Returns:
        ConversationManager: Konuşma yöneticisi
    """
    return ConversationManager()