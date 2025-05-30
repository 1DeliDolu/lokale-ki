"""
Ana ChatGPT benzeri sohbet botu sınıfı
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GPT2LMHeadModel, GPT2Tokenizer
from typing import Optional, Dict, Any, List
import logging
import time
import threading

from .config import ChatbotConfig, ConversationConfig
from .utils import ChatUtils, ConversationHistory, ResponseGenerator
from .exceptions import (
    ModelLoadError, 
    ConversationError, 
    GenerationTimeoutError, 
    InvalidInputError
)

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatGPTLikeBot:
    """
    ChatGPT benzeri sohbet botu sınıfı
    
    Hugging Face transformers kullanarak açık kaynak modeller ile
    doğal dil konuşması yapabilir.
    """
    
    def __init__(
        self, 
        config: Optional[ChatbotConfig] = None,
        model_name: Optional[str] = None
    ):
        """
        Sohbet botunu başlat
        
        Args:
            config (ChatbotConfig, optional): Bot konfigürasyonu
            model_name (str, optional): Kullanılacak model adı
        """
        # Konfigürasyon ayarla
        if config is None:
            config = ChatbotConfig()
        
        if model_name:
            config.model_name = model_name
        
        self.config = config
        
        # Model ve tokenizer'ı yükle
        self._load_model()
        
        # Konuşma geçmişini başlat
        self.conversation_history = ConversationHistory()
        
        logger.info(f"✅ ChatGPT-like Bot başlatıldı - Model: {self.config.model_name}")
    
    def _load_model(self) -> None:
        """Model ve tokenizer'ı yükle"""
        try:
            logger.info(f"🤖 Model yükleniyor: {self.config.model_name}")
            
            # Device ayarları
            if self.config.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            else:
                self.device = self.config.device
            
            # Model türüne göre yükleme
            if "DialoGPT" in self.config.model_name:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.config.model_name,
                    cache_dir=self.config.cache_dir,
                    padding_side='left'
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.config.model_name,
                    cache_dir=self.config.cache_dir
                )
            else:
                # Genel GPT modelleri için
                self.tokenizer = GPT2Tokenizer.from_pretrained(
                    self.config.model_name,
                    cache_dir=self.config.cache_dir
                )
                self.model = GPT2LMHeadModel.from_pretrained(
                    self.config.model_name,
                    cache_dir=self.config.cache_dir
                )
            
            # Pad token ayarla
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"📱 Device: {self.device}")
            
        except Exception as e:
            raise ModelLoadError(self.config.model_name, str(e))
    
    def chat(
        self, 
        message: str, 
        conversation_id: Optional[str] = None,
        use_history: bool = True
    ) -> str:
        """
        Kullanıcı ile sohbet et
        
        Args:
            message (str): Kullanıcı mesajı
            conversation_id (str, optional): Konuşma ID'si
            use_history (bool): Konuşma geçmişi kullanılsın mı
            
        Returns:
            str: Bot yanıtı
        """
        try:
            # Girişi doğrula
            if not message or not message.strip():
                raise InvalidInputError("message", "Boş mesaj")
            
            message = ChatUtils.clean_text(message)
            intent = ChatUtils.extract_intent(message)
            
            # Konuşma geçmişine ekle
            if conversation_id is None and use_history:
                conversation_id = self.conversation_history.current_conversation_id
                if conversation_id is None:
                    conversation_id = self.conversation_history.create_conversation()
            
            if use_history and conversation_id:
                self.conversation_history.add_message("user", message, conversation_id)
            
            # Yanıt üret
            response = self._generate_response(message, conversation_id if use_history else None)
            
            # Yanıtı formatla
            formatted_response = ChatUtils.format_response(response, intent)
            
            # Konuşma geçmişine ekle
            if use_history and conversation_id:
                self.conversation_history.add_message("assistant", formatted_response, conversation_id)
            
            logger.info(f"✅ Yanıt üretildi - Intent: {intent}")
            return formatted_response
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Sohbet hatası: {error_msg}")
            
            # Fallback yanıt
            try:
                intent = ChatUtils.extract_intent(message) if message else 'general'
                return ResponseGenerator.generate_fallback_response(intent, message)
            except:
                return "Üzgünüm, şu anda size yardımcı olamıyorum. Lütfen daha sonra tekrar deneyin."
    
    def _generate_response(self, message: str, conversation_id: str = None) -> str:
        """
        Yanıt üret (AI model kullanarak)
        
        Args:
            message (str): Kullanıcı mesajı
            conversation_id (str, optional): Konuşma ID'si
            
        Returns:
            str: Üretilen yanıt
        """
        try:
            # Konuşma geçmişini al
            chat_history = []
            if conversation_id:
                recent_messages = self.conversation_history.get_recent_messages(
                    self.config.conversation_history_limit, 
                    conversation_id
                )
                chat_history = [msg['content'] for msg in recent_messages[-5:]]  # Son 5 mesaj
            
            # Input metni hazırla
            if "DialoGPT" in self.config.model_name:
                # DialoGPT için özel format
                if chat_history:
                    input_text = " <|endoftext|> ".join(chat_history + [message]) + " <|endoftext|>"
                else:
                    input_text = message + " <|endoftext|>"
            else:
                # Genel GPT için
                if chat_history:
                    input_text = f"Konuşma geçmişi: {' '.join(chat_history[-3:])} Kullanıcı: {message} Asistan:"
                else:
                    input_text = f"Kullanıcı: {message} Asistan:"
            
            # Tokenize et
            inputs = self.tokenizer.encode(
                input_text, 
                return_tensors="pt",
                max_length=self.config.max_length - self.config.max_new_tokens,
                truncation=True
            ).to(self.device)
            
            # Yanıt üret
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=self.config.max_new_tokens,
                    num_beams=self.config.num_beams,
                    do_sample=self.config.do_sample,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    top_k=self.config.top_k,
                    repetition_penalty=self.config.repetition_penalty,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    early_stopping=True
                )
            
            # Yanıtı decode et
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Sadece yeni üretilen kısmı al
            if "DialoGPT" in self.config.model_name:
                response = response.replace(input_text, "").strip()
            else:
                # Asistan: kısmından sonrasını al
                if "Asistan:" in response:
                    response = response.split("Asistan:")[-1].strip()
            
            # Boş yanıt kontrolü
            if not response or len(response.strip()) < 2:
                raise ConversationError("Boş yanıt üretildi")
            
            return response.strip()
            
        except Exception as e:
            raise ConversationError("response_generation", str(e))
    
    def start_new_conversation(self, title: str = None) -> str:
        """
        Yeni konuşma başlat
        
        Args:
            title (str, optional): Konuşma başlığı
            
        Returns:
            str: Konuşma ID'si
        """
        return self.conversation_history.create_conversation(title)
    
    def get_conversation_list(self) -> List[Dict]:
        """
        Konuşma listesini getir
        
        Returns:
            list: Konuşma listesi
        """
        return self.conversation_history.list_conversations()
    
    def get_conversation(self, conversation_id: str) -> Dict:
        """
        Belirli bir konuşmayı getir
        
        Args:
            conversation_id (str): Konuşma ID'si
            
        Returns:
            dict: Konuşma verisi
        """
        return self.conversation_history.get_conversation(conversation_id)
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Konuşmayı sil
        
        Args:
            conversation_id (str): Konuşma ID'si
            
        Returns:
            bool: Başarılı ise True
        """
        return self.conversation_history.delete_conversation(conversation_id)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Model bilgilerini getir
        
        Returns:
            dict: Model bilgileri
        """
        return {
            'model_name': self.config.model_name,
            'device': self.device,
            'cuda_available': torch.cuda.is_available(),
            'config': self.config.to_dict()
        }

class ConversationManager:
    """
    Çoklu konuşma yöneticisi
    """
    
    def __init__(self, config: Optional[ConversationConfig] = None):
        """
        Konuşma yöneticisini başlat
        
        Args:
            config (ConversationConfig, optional): Konuşma konfigürasyonu
        """
        self.config = config or ConversationConfig()
        self.conversations: Dict[str, ConversationHistory] = {}
        self.bots: Dict[str, ChatGPTLikeBot] = {}
    
    def create_bot(
        self, 
        bot_id: str, 
        config: Optional[ChatbotConfig] = None
    ) -> ChatGPTLikeBot:
        """
        Yeni bot oluştur
        
        Args:
            bot_id (str): Bot ID'si
            config (ChatbotConfig, optional): Bot konfigürasyonu
            
        Returns:
            ChatGPTLikeBot: Oluşturulan bot
        """
        bot = ChatGPTLikeBot(config)
        self.bots[bot_id] = bot
        return bot
    
    def get_bot(self, bot_id: str) -> Optional[ChatGPTLikeBot]:
        """
        Bot'u getir
        
        Args:
            bot_id (str): Bot ID'si
            
        Returns:
            ChatGPTLikeBot: Bot instance'ı
        """
        return self.bots.get(bot_id)
    
    def chat_with_bot(
        self, 
        bot_id: str, 
        message: str, 
        conversation_id: str = None
    ) -> str:
        """
        Belirli bir bot ile sohbet et
        
        Args:
            bot_id (str): Bot ID'si
            message (str): Kullanıcı mesajı
            conversation_id (str, optional): Konuşma ID'si
            
        Returns:
            str: Bot yanıtı
        """
        bot = self.get_bot(bot_id)
        if not bot:
            raise ConversationError(f"Bot bulunamadı: {bot_id}")
        
        return bot.chat(message, conversation_id)
    
    def list_bots(self) -> List[str]:
        """
        Bot listesini getir
        
        Returns:
            list: Bot ID'leri
        """
        return list(self.bots.keys())