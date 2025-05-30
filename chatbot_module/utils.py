"""
Sohbet botu yardımcı fonksiyonlar ve araçlar
"""

import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import random

from .exceptions import ConversationHistoryError, InvalidInputError

class ChatUtils:
    """
    Sohbet işleme yardımcı fonksiyonları
    """
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Metni temizle ve formatla
        
        Args:
            text (str): Ham metin
            
        Returns:
            str: Temizlenmiş metin
        """
        if not isinstance(text, str):
            return ""
        
        # Fazla boşlukları temizle
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Tekrarlayan noktalama işaretlerini temizle
        text = re.sub(r'([.!?])\1+', r'\1', text)
        
        # Emoji'leri koru ama fazla sembolleri temizle
        text = re.sub(r'[^\w\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF.,!?;:()"-]', '', text)
        
        return text.strip()
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Metindeki dili tespit et (basit)
        
        Args:
            text (str): Metin
            
        Returns:
            str: Dil kodu ('tr', 'en', 'unknown')
        """
        # Türkçe karakterler
        turkish_chars = set('çğıöşüÇĞIİÖŞÜ')
        
        # İngilizce yaygın kelimeler
        english_words = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with', 'for', 'as', 'was', 'on', 'are'}
        
        # Türkçe yaygın kelimeler
        turkish_words = {'bir', 've', 'bu', 'da', 'de', 'ile', 'mi', 'mı', 'ne', 'o', 'var', 'yok', 'ben', 'sen', 'biz'}
        
        text_lower = text.lower()
        words = set(text_lower.split())
        
        # Türkçe karakter kontrolü
        if any(char in text for char in turkish_chars):
            return 'tr'
        
        # Kelime bazlı kontrol
        english_score = len(words & english_words)
        turkish_score = len(words & turkish_words)
        
        if turkish_score > english_score:
            return 'tr'
        elif english_score > turkish_score:
            return 'en'
        
        return 'unknown'
    
    @staticmethod
    def extract_intent(text: str) -> str:
        """
        Metinden niyet çıkar (basit)
        
        Args:
            text (str): Kullanıcı metni
            
        Returns:
            str: Tespit edilen niyet
        """
        text_lower = text.lower()
        
        # Selamlama
        greetings = ['merhaba', 'selam', 'günaydın', 'iyi günler', 'naber', 'nasılsın']
        if any(word in text_lower for word in greetings):
            return 'greeting'
        
        # Veda
        farewells = ['görüşürüz', 'bay', 'güle güle', 'hoşça kal', 'elveda']
        if any(word in text_lower for word in farewells):
            return 'farewell'
        
        # Soru
        question_words = ['nasıl', 'ne', 'neden', 'nerede', 'kim', 'hangi', 'kaç']
        if any(word in text_lower for word in question_words) or text.endswith('?'):
            return 'question'
        
        # Yardım isteği
        help_words = ['yardım', 'help', 'nasıl yapılır', 'öğren', 'anlat']
        if any(word in text_lower for word in help_words):
            return 'help_request'
        
        # Teşekkür
        thanks = ['teşekkür', 'sağol', 'mersi', 'thanks']
        if any(word in text_lower for word in thanks):
            return 'thanks'
        
        return 'general'
    
    @staticmethod
    def format_response(response: str, intent: str = 'general') -> str:
        """
        Yanıtı formatla ve iyileştir
        
        Args:
            response (str): Ham yanıt
            intent (str): Tespit edilen niyet
            
        Returns:
            str: Formatlanmış yanıt
        """
        if not response:
            return "Üzgünüm, bir yanıt oluşturamadım."
        
        # Metni temizle
        response = ChatUtils.clean_text(response)
        
        # Çok kısa yanıtları genişlet
        if len(response) < 10:
            intent_responses = {
                'greeting': f"{response} Size nasıl yardımcı olabilirim?",
                'thanks': f"{response} Başka bir sorunuz var mı?",
                'farewell': f"{response} İyi günler!",
                'general': f"{response} Başka bir şey sormak ister misiniz?"
            }
            response = intent_responses.get(intent, response)
        
        # İlk harfi büyük yap
        if response and not response[0].isupper():
            response = response[0].upper() + response[1:]
        
        # Noktalama ekle
        if response and not response.endswith(('.', '!', '?')):
            response += '.'
        
        return response

class ConversationHistory:
    """
    Konuşma geçmişi yönetimi
    """
    
    def __init__(self, file_path: str = "conversations.json"):
        self.file_path = file_path
        self.conversations: Dict[str, Dict] = {}
        self.current_conversation_id: Optional[str] = None
        self.load_conversations()
    
    def create_conversation(self, title: str = None) -> str:
        """
        Yeni konuşma oluştur
        
        Args:
            title (str, optional): Konuşma başlığı
            
        Returns:
            str: Konuşma ID'si
        """
        conversation_id = str(uuid.uuid4())
        
        if not title:
            title = f"Konuşma {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        self.conversations[conversation_id] = {
            'id': conversation_id,
            'title': title,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'messages': []
        }
        
        self.current_conversation_id = conversation_id
        self.save_conversations()
        return conversation_id
    
    def add_message(self, role: str, content: str, conversation_id: str = None) -> None:
        """
        Konuşmaya mesaj ekle
        
        Args:
            role (str): 'user' veya 'assistant'
            content (str): Mesaj içeriği
            conversation_id (str, optional): Konuşma ID'si
        """
        if conversation_id is None:
            conversation_id = self.current_conversation_id
        
        if conversation_id is None:
            conversation_id = self.create_conversation()
        
        if conversation_id not in self.conversations:
            raise ConversationHistoryError(f"Konuşma bulunamadı: {conversation_id}")
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        self.conversations[conversation_id]['messages'].append(message)
        self.conversations[conversation_id]['updated_at'] = datetime.now().isoformat()
        
        # Başlığı ilk kullanıcı mesajından oluştur
        if role == 'user' and len(self.conversations[conversation_id]['messages']) == 1:
            title = content[:50] + "..." if len(content) > 50 else content
            self.conversations[conversation_id]['title'] = title
        
        self.save_conversations()
    
    def get_conversation(self, conversation_id: str) -> Dict:
        """
        Konuşmayı getir
        
        Args:
            conversation_id (str): Konuşma ID'si
            
        Returns:
            dict: Konuşma verisi
        """
        if conversation_id not in self.conversations:
            raise ConversationHistoryError(f"Konuşma bulunamadı: {conversation_id}")
        
        return self.conversations[conversation_id]
    
    def get_recent_messages(self, limit: int = 10, conversation_id: str = None) -> List[Dict]:
        """
        Son mesajları getir
        
        Args:
            limit (int): Mesaj sayısı limiti
            conversation_id (str, optional): Konuşma ID'si
            
        Returns:
            list: Mesaj listesi
        """
        if conversation_id is None:
            conversation_id = self.current_conversation_id
        
        if conversation_id is None or conversation_id not in self.conversations:
            return []
        
        messages = self.conversations[conversation_id]['messages']
        return messages[-limit:] if limit > 0 else messages
    
    def list_conversations(self, limit: int = 50) -> List[Dict]:
        """
        Konuşmaları listele
        
        Args:
            limit (int): Konuşma sayısı limiti
            
        Returns:
            list: Konuşma listesi
        """
        conversations = list(self.conversations.values())
        conversations.sort(key=lambda x: x['updated_at'], reverse=True)
        return conversations[:limit]
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Konuşmayı sil
        
        Args:
            conversation_id (str): Konuşma ID'si
            
        Returns:
            bool: Başarılı ise True
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            if self.current_conversation_id == conversation_id:
                self.current_conversation_id = None
            self.save_conversations()
            return True
        return False
    
    def save_conversations(self) -> None:
        """Konuşmaları dosyaya kaydet"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ConversationHistoryError("save", str(e))
    
    def load_conversations(self) -> None:
        """Konuşmaları dosyadan yükle"""
        try:
            if Path(self.file_path).exists():
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.conversations = json.load(f)
        except Exception as e:
            # Dosya yok veya bozuksa boş başla
            self.conversations = {}

class ResponseGenerator:
    """
    Otomatik yanıt üretici (fallback için)
    """
    
    @staticmethod
    def generate_fallback_response(intent: str, user_message: str) -> str:
        """
        Model başarısız olduğunda kullanılacak fallback yanıt
        
        Args:
            intent (str): Tespit edilen niyet
            user_message (str): Kullanıcı mesajı
            
        Returns:
            str: Fallback yanıt
        """
        responses = {
            'greeting': [
                "Merhaba! Size nasıl yardımcı olabilirim?",
                "Selam! Bugün nasılsınız?",
                "Hoş geldiniz! Hangi konuda yardım edebilirim?"
            ],
            'farewell': [
                "Görüşmek üzere! İyi günler!",
                "Hoşça kalın! Tekrar bekleriz.",
                "Güle güle! İyi günler dilerim."
            ],
            'thanks': [
                "Rica ederim! Başka bir şey için yardıma ihtiyacınız var mı?",
                "Ne demek! Size nasıl daha fazla yardımcı olabilirim?",
                "Memnun oldum yardımcı olabildiğime!"
            ],
            'help_request': [
                "Tabii ki yardımcı olmaya çalışırım! Daha spesifik olabilir misiniz?",
                "Size yardımcı olmak isterim. Hangi konuda bilgi almak istiyorsunuz?",
                "Elbette! Neyle ilgili yardım istiyorsunuz?"
            ],
            'question': [
                "İlginç bir soru! Bu konuda elimden geldiğince yardımcı olmaya çalışırım.",
                "Bu sorunuz hakkında düşünüyorum. Daha detay verebilir misiniz?",
                "Güzel bir soru! Bu konuda bilgilerimi paylaşmaya çalışırım."
            ],
            'general': [
                "Anlıyorum. Bu konuda daha fazla bilgi verebilir misiniz?",
                "İlginç! Bu konu hakkında konuşmak güzel.",
                "Hmm, bu konuda ne düşünüyorsunuz?"
            ]
        }
        
        intent_responses = responses.get(intent, responses['general'])
        return random.choice(intent_responses)