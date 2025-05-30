"""
Sohbet botu konfigürasyon sınıfları
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class ChatbotConfig:
    """
    Sohbet botu konfigürasyonu
    """
    model_name: str = "microsoft/DialoGPT-medium"
    device: str = "auto"  # "auto", "cpu", "cuda"
    cache_dir: Optional[str] = None
    
    # Generation parametreleri
    max_length: int = 1000
    max_new_tokens: int = 100
    num_beams: int = 1
    do_sample: bool = True
    temperature: float = 0.8
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    
    # Konuşma ayarları
    conversation_history_limit: int = 10
    response_timeout: int = 30
    
    # Sistem mesajı
    system_message: str = "Sen yardımsever bir yapay zeka asistanısın. Türkçe olarak yanıt ver."
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük olarak döndür"""
        return {
            'model_name': self.model_name,
            'device': self.device,
            'cache_dir': self.cache_dir,
            'max_length': self.max_length,
            'max_new_tokens': self.max_new_tokens,
            'num_beams': self.num_beams,
            'do_sample': self.do_sample,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'top_k': self.top_k,
            'repetition_penalty': self.repetition_penalty,
            'conversation_history_limit': self.conversation_history_limit,
            'response_timeout': self.response_timeout,
            'system_message': self.system_message
        }

@dataclass
class ConversationConfig:
    """
    Konuşma yönetimi konfigürasyonu
    """
    save_conversations: bool = True
    conversation_file: str = "conversations.json"
    max_conversations: int = 100
    auto_save: bool = True
    
    # Konuşma formatı
    timestamp_format: str = "%Y-%m-%d %H:%M:%S"
    conversation_title_length: int = 50
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük olarak döndür"""
        return {
            'save_conversations': self.save_conversations,
            'conversation_file': self.conversation_file,
            'max_conversations': self.max_conversations,
            'auto_save': self.auto_save,
            'timestamp_format': self.timestamp_format,
            'conversation_title_length': self.conversation_title_length
        }

class ModelPresets:
    """
    Önceden tanımlı model konfigürasyonları
    """
    
    @staticmethod
    def conversational_model() -> ChatbotConfig:
        """Sohbet odaklı model"""
        return ChatbotConfig(
            model_name="microsoft/DialoGPT-medium",
            temperature=0.8,
            max_new_tokens=150,
            system_message="Sen arkadaş canlısı bir sohbet botsun. Samimi ve yardımsever bir şekilde konuş."
        )
    
    @staticmethod
    def helpful_assistant() -> ChatbotConfig:
        """Yardımcı asistan modeli"""
        return ChatbotConfig(
            model_name="microsoft/DialoGPT-large",
            temperature=0.6,
            max_new_tokens=200,
            repetition_penalty=1.2,
            system_message="Sen bilgili ve yardımsever bir asistansın. Detaylı ve doğru yanıtlar ver."
        )
    
    @staticmethod
    def creative_writer() -> ChatbotConfig:
        """Yaratıcı yazım modeli"""
        return ChatbotConfig(
            model_name="microsoft/DialoGPT-large",
            temperature=1.0,
            top_p=0.95,
            max_new_tokens=300,
            system_message="Sen yaratıcı bir yazarsın. İlginç hikayeler ve açıklamalar yaz."
        )
    
    @staticmethod
    def technical_expert() -> ChatbotConfig:
        """Teknik uzman modeli"""
        return ChatbotConfig(
            model_name="microsoft/DialoGPT-large",
            temperature=0.4,
            max_new_tokens=250,
            repetition_penalty=1.1,
            system_message="Sen teknik konularda uzman bir asistansın. Programlama ve teknoloji sorularına detaylı yanıt ver."
        )
    
    @staticmethod
    def fast_chat() -> ChatbotConfig:
        """Hızlı sohbet modeli"""
        return ChatbotConfig(
            model_name="microsoft/DialoGPT-small",
            temperature=0.7,
            max_new_tokens=80,
            num_beams=1,
            system_message="Sen hızlı ve öz yanıtlar veren bir botsun."
        )

class PromptTemplates:
    """
    Hazır prompt şablonları
    """
    
    CONVERSATION_STARTER = [
        "Merhaba! Size nasıl yardımcı olabilirim?",
        "Selam! Bugün hangi konuda konuşmak istersiniz?",
        "Hoş geldiniz! Size nasıl destek olabilirim?",
        "Merhaba! Hangi sorunuzla ilgili yardım edebilirim?"
    ]
    
    ERROR_RESPONSES = [
        "Üzgünüm, bir sorun yaşıyorum. Lütfen tekrar deneyin.",
        "Anlayamadım, sorunuzu farklı şekilde sorabilir misiniz?",
        "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.",
        "Bu konuda size yardımcı olamıyorum. Başka bir şey deneyebiliriz."
    ]
    
    THINKING_RESPONSES = [
        "Düşünüyorum...",
        "Bir dakika, yanıtınızı hazırlıyorum...",
        "İşleniyor...",
        "Yanıtınızı oluşturuyorum..."
    ]

# Türkçe dil ayarları
class TurkishLanguageConfig:
    """
    Türkçe dil özel ayarları
    """
    
    GREETING_PATTERNS = [
        "merhaba", "selam", "selamlar", "naber", "nasılsın",
        "günaydın", "iyi günler", "iyi akşamlar", "iyi geceler"
    ]
    
    FAREWELL_PATTERNS = [
        "görüşürüz", "hoşça kal", "bay bay", "elveda", "güle güle",
        "iyi günler", "iyi akşamlar", "iyi geceler"
    ]
    
    POLITENESS_WORDS = [
        "lütfen", "teşekkürler", "sağol", "mersi", "rica ederim",
        "özür dilerim", "pardon", "kusura bakma"
    ]