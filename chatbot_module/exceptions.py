"""
Sohbet botu özel istisna sınıfları
"""

class ChatbotError(Exception):
    """
    Genel sohbet botu hatası
    """
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message

class ModelLoadError(ChatbotError):
    """
    Model yükleme hatası
    """
    def __init__(self, model_name: str, original_error: str = None):
        message = f"Sohbet modeli yüklenemedi: {model_name}"
        if original_error:
            message += f" - {original_error}"
        super().__init__(message, "MODEL_LOAD_ERROR")

class ConversationError(ChatbotError):
    """
    Konuşma işleme hatası
    """
    def __init__(self, operation: str, original_error: str = None):
        message = f"Konuşma işlemi başarısız: {operation}"
        if original_error:
            message += f" - {original_error}"
        super().__init__(message, "CONVERSATION_ERROR")

class GenerationTimeoutError(ChatbotError):
    """
    Yanıt üretme zaman aşımı hatası
    """
    def __init__(self, timeout_seconds: int):
        message = f"Yanıt üretme zaman aşımı: {timeout_seconds} saniye"
        super().__init__(message, "GENERATION_TIMEOUT")

class InvalidInputError(ChatbotError):
    """
    Geçersiz giriş hatası
    """
    def __init__(self, input_type: str, value: str):
        message = f"Geçersiz {input_type}: {value}"
        super().__init__(message, "INVALID_INPUT")

class ConversationHistoryError(ChatbotError):
    """
    Konuşma geçmişi hatası
    """
    def __init__(self, operation: str, original_error: str = None):
        message = f"Konuşma geçmişi işlemi başarısız: {operation}"
        if original_error:
            message += f" - {original_error}"
        super().__init__(message, "CONVERSATION_HISTORY_ERROR")