"""
Yardımcı fonksiyonlar ve araçlar
"""

import numpy as np
import os
import re
from pathlib import Path
from PIL import Image
from typing import Union, List, Optional, Tuple
from datetime import datetime

from .exceptions import ImageProcessingError, FileOperationError, ValidationError

class ImageUtils:
    """
    Görsel işleme yardımcı fonksiyonları
    """
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    
    @staticmethod
    def validate_image_path(image_path: str) -> bool:
        """
        Görsel dosya yolunu doğrula
        
        Args:
            image_path (str): Dosya yolu
            
        Returns:
            bool: Geçerli ise True
            
        Raises:
            ValidationError: Geçersiz dosya yolu
        """
        if not isinstance(image_path, str):
            raise ValidationError("image_path", str(type(image_path)), "string")
        
        if not os.path.exists(image_path):
            raise ValidationError("image_path", image_path, "existing file")
        
        # Dosya uzantısını kontrol et
        ext = Path(image_path).suffix.lower()
        if ext not in ImageUtils.SUPPORTED_FORMATS:
            raise ValidationError(
                "file_extension", 
                ext, 
                f"one of {ImageUtils.SUPPORTED_FORMATS}"
            )
        
        return True
    
    @staticmethod
    def preprocess_image(
        input_image: Union[str, np.ndarray, Image.Image], 
        max_size: int = 512
    ) -> Image.Image:
        """
        Görseli işleme için hazırla
        
        Args:
            input_image: Görsel (dosya yolu, numpy array veya PIL Image)
            max_size (int): Maksimum boyut
            
        Returns:
            PIL.Image: İşlenmiş görsel
            
        Raises:
            ImageProcessingError: İşleme hatası
        """
        try:
            # Tip kontrolü ve dönüşüm
            if isinstance(input_image, str):
                ImageUtils.validate_image_path(input_image)
                raw_image = Image.open(input_image).convert('RGB')
            elif isinstance(input_image, np.ndarray):
                raw_image = Image.fromarray(input_image.astype('uint8')).convert('RGB')
            elif isinstance(input_image, Image.Image):
                raw_image = input_image.convert('RGB')
            else:
                raise ValidationError(
                    "input_image", 
                    str(type(input_image)), 
                    "str, np.ndarray, or PIL.Image"
                )
            
            # Boyut kontrolü ve yeniden boyutlandırma
            if max(raw_image.size) > max_size:
                raw_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            return raw_image
            
        except Exception as e:
            if isinstance(e, (ValidationError, ImageProcessingError)):
                raise
            raise ImageProcessingError(str(input_image), str(e))
    
    @staticmethod
    def get_image_info(image: Union[str, Image.Image, np.ndarray]) -> dict:
        """
        Görsel bilgilerini al
        
        Args:
            image: Görsel dosyası, PIL Image veya numpy array
            
        Returns:
            dict: Görsel bilgileri
        """
        try:
            if isinstance(image, str):
                img = Image.open(image)
                file_size = os.path.getsize(image)
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'file_size': file_size
                }
            elif isinstance(image, np.ndarray):
                # Numpy array için bilgiler
                height, width = image.shape[:2]
                channels = image.shape[2] if len(image.shape) > 2 else 1
                return {
                    'format': 'numpy_array',
                    'mode': f'RGB' if channels == 3 else f'{channels}_channel',
                    'size': (width, height),
                    'width': width,
                    'height': height,
                    'file_size': None,
                    'dtype': str(image.dtype),
                    'shape': image.shape
                }
            else:
                # PIL Image
                img = image
                file_size = None
                return {
                    'format': img.format or 'PIL_Image',
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'file_size': file_size
                }
            
        except Exception as e:
            # Hata durumunda basit bilgi döndür
            return {
                'format': 'unknown',
                'mode': 'unknown',
                'size': (0, 0),
                'width': 0,
                'height': 0,
                'file_size': None,
                'error': str(e)
            }

class FileUtils:
    """
    Dosya işleme yardımcı fonksiyonları
    """
    
    @staticmethod
    def create_safe_filename(text: str, max_length: int = 50) -> str:
        """
        Güvenli dosya adı oluştur
        
        Args:
            text (str): Metin
            max_length (int): Maksimum uzunluk
            
        Returns:
            str: Güvenli dosya adı
        """
        # Özel karakterleri temizle
        safe_text = re.sub(r'[^\w\s-]', '', text).strip()
        safe_text = re.sub(r'[-\s]+', '_', safe_text)
        
        # Uzunluk kontrolü
        if len(safe_text) > max_length:
            safe_text = safe_text[:max_length]
        
        # Boş veya çok kısa ise varsayılan isim
        if not safe_text or len(safe_text) < 3:
            safe_text = "image_caption"
        
        return safe_text
    
    @staticmethod
    def get_unique_filepath(file_path: str) -> str:
        """
        Benzersiz dosya yolu oluştur
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            str: Benzersiz dosya yolu
        """
        if not os.path.exists(file_path):
            return file_path
        
        base_path = Path(file_path)
        name = base_path.stem
        ext = base_path.suffix
        parent = base_path.parent
        
        counter = 1
        while True:
            new_path = parent / f"{name}_{counter}{ext}"
            if not new_path.exists():
                return str(new_path)
            counter += 1
    
    @staticmethod
    def ensure_directory(directory_path: str) -> str:
        """
        Klasörün var olduğundan emin ol, yoksa oluştur
        
        Args:
            directory_path (str): Klasör yolu
            
        Returns:
            str: Klasör yolu
            
        Raises:
            FileOperationError: Klasör oluşturma hatası
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            return directory_path
        except Exception as e:
            raise FileOperationError("create_directory", directory_path, str(e))
    
    @staticmethod
    def save_metadata(
        file_path: str, 
        title: str, 
        caption: str, 
        model_name: str,
        additional_info: Optional[dict] = None
    ) -> str:
        """
        Metadata dosyasını kaydet
        
        Args:
            file_path (str): Ana dosya yolu
            title (str): Başlık
            caption (str): Açıklama
            model_name (str): Model adı
            additional_info (dict, optional): Ek bilgiler
            
        Returns:
            str: Metadata dosya yolu
            
        Raises:
            FileOperationError: Kaydetme hatası
        """
        try:
            metadata_file = str(Path(file_path).with_suffix('.txt'))
            metadata_file = metadata_file.replace('.jpg.txt', '_metadata.txt')
            metadata_file = metadata_file.replace('.png.txt', '_metadata.txt')
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                f.write(f"Dosya: {os.path.basename(file_path)}\n")
                f.write(f"Başlık: {title}\n")
                f.write(f"Açıklama: {caption}\n")
                f.write(f"Model: {model_name}\n")
                f.write(f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                if additional_info:
                    f.write("\n--- Ek Bilgiler ---\n")
                    for key, value in additional_info.items():
                        f.write(f"{key}: {value}\n")
            
            return metadata_file
            
        except Exception as e:
            raise FileOperationError("save_metadata", file_path, str(e))
    
    @staticmethod
    def find_images_in_directory(directory: str, recursive: bool = False) -> List[str]:
        """
        Klasörde görsel dosyalarını bul
        
        Args:
            directory (str): Klasör yolu
            recursive (bool): Alt klasörleri de tara
            
        Returns:
            List[str]: Görsel dosya yolları
        """
        if not os.path.exists(directory):
            raise ValidationError("directory", directory, "existing directory")
        
        image_files = []
        search_pattern = "**/*" if recursive else "*"
        
        for ext in ImageUtils.SUPPORTED_FORMATS:
            pattern = str(Path(directory) / search_pattern) + ext
            image_files.extend(Path(directory).glob(pattern))
            
            # Büyük harf versiyonları da ekle
            pattern = str(Path(directory) / search_pattern) + ext.upper()
            image_files.extend(Path(directory).glob(pattern))
        
        return [str(f) for f in image_files]

class ProgressTracker:
    """
    İlerleme takibi için yardımcı sınıf
    """
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
    
    def update(self, step: int = 1) -> None:
        """İlerlemeyi güncelle"""
        self.current += step
        self._print_progress()
    
    def _print_progress(self) -> None:
        """İlerlemeyi yazdır"""
        percentage = (self.current / self.total) * 100
        bar_length = 30
        filled_length = int(bar_length * self.current // self.total)
        
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        print(f'\r{self.description}: |{bar}| {self.current}/{self.total} ({percentage:.1f}%)', end='')
        
        if self.current >= self.total:
            print()  # Yeni satır