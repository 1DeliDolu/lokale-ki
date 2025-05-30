"""
Özel istisna sınıfları
"""

class ImageAnalysisError(Exception):
    """
    Genel görsel analiz hatası
    """
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message

class ModelLoadError(ImageAnalysisError):
    """
    Model yükleme hatası
    """
    def __init__(self, model_name: str, original_error: str = None):
        message = f"Model yüklenemedi: {model_name}"
        if original_error:
            message += f" - {original_error}"
        super().__init__(message, "MODEL_LOAD_ERROR")

class ImageProcessingError(ImageAnalysisError):
    """
    Görsel işleme hatası
    """
    def __init__(self, image_path: str, original_error: str = None):
        message = f"Görsel işlenemedi: {image_path}"
        if original_error:
            message += f" - {original_error}"
        super().__init__(message, "IMAGE_PROCESSING_ERROR")

class GenerationError(ImageAnalysisError):
    """
    Açıklama üretme hatası
    """
    def __init__(self, operation: str, original_error: str = None):
        message = f"{operation} işlemi başarısız"
        if original_error:
            message += f" - {original_error}"
        super().__init__(message, "GENERATION_ERROR")

class FileOperationError(ImageAnalysisError):
    """
    Dosya işlemi hatası
    """
    def __init__(self, operation: str, file_path: str, original_error: str = None):
        message = f"{operation} işlemi başarısız: {file_path}"
        if original_error:
            message += f" - {original_error}"
        super().__init__(message, "FILE_OPERATION_ERROR")

class ValidationError(ImageAnalysisError):
    """
    Doğrulama hatası
    """
    def __init__(self, parameter: str, value: str, expected: str = None):
        message = f"Geçersiz parametre - {parameter}: {value}"
        if expected:
            message += f" (Beklenen: {expected})"
        super().__init__(message, "VALIDATION_ERROR")