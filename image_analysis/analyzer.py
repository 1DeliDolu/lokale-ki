"""
Ana görsel analiz sınıfı - Yeniden düzenlenmiş ve geliştirilmiş versiyon
"""

import torch
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
from typing import Union, List, Dict, Any, Optional
import logging

from .config import ModelConfig, AnalysisConfig
from .utils import ImageUtils, FileUtils, ProgressTracker
from .exceptions import (
    ModelLoadError, 
    ImageProcessingError, 
    GenerationError, 
    FileOperationError
)

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """
    Gelişmiş görsel analizi ve açıklama üretimi sınıfı
    """
    
    def __init__(
        self, 
        model_config: Optional[ModelConfig] = None,
        analysis_config: Optional[AnalysisConfig] = None
    ):
        """
        Analyzer'ı başlat
        
        Args:
            model_config (ModelConfig, optional): Model konfigürasyonu
            analysis_config (AnalysisConfig, optional): Analiz konfigürasyonu
        """
        self.model_config = model_config or ModelConfig()
        self.analysis_config = analysis_config or AnalysisConfig()
        
        # Model ve processor'u yükle
        self._load_model()
        
        logger.info(f"✅ ImageAnalyzer başlatıldı - Model: {self.model_config.model_name}")
    
    def _load_model(self) -> None:
        """Model ve processor'u yükle"""
        try:
            logger.info(f"🤖 Model yükleniyor: {self.model_config.model_name}")
            
            # Processor yükle
            self.processor = AutoProcessor.from_pretrained(
                self.model_config.model_name,
                cache_dir=self.model_config.cache_dir,
                use_auth_token=self.model_config.use_auth_token
            )
            
            # Model yükle
            self.model = BlipForConditionalGeneration.from_pretrained(
                self.model_config.model_name,
                cache_dir=self.model_config.cache_dir,
                use_auth_token=self.model_config.use_auth_token
            )
            
            # Device ayarları
            if self.model_config.device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            else:
                self.device = self.model_config.device
            
            self.model.to(self.device)
            logger.info(f"📱 Device: {self.device}")
            
        except Exception as e:
            raise ModelLoadError(self.model_config.model_name, str(e))
    
    def generate_caption(
        self, 
        image: Union[str, Image.Image], 
        conditional_text: str = ""
    ) -> str:
        """
        Görsel için açıklama üret
        
        Args:
            image: Görsel dosyası
            conditional_text (str): Koşullu metin
            
        Returns:
            str: Üretilen açıklama
            
        Raises:
            GenerationError: Üretim hatası
        """
        try:
            # Görseli işle
            processed_image = ImageUtils.preprocess_image(
                image, 
                self.analysis_config.max_image_size
            )
            
            # Model girişi hazırla
            if conditional_text:
                inputs = self.processor(
                    images=processed_image, 
                    text=conditional_text, 
                    return_tensors="pt"
                ).to(self.device)
            else:
                inputs = self.processor(
                    images=processed_image, 
                    return_tensors="pt"
                ).to(self.device)
            
            # Açıklama üret
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=self.model_config.max_length,
                    num_beams=self.model_config.num_beams,
                    do_sample=self.model_config.do_sample,
                    early_stopping=self.model_config.early_stopping,
                    temperature=self.model_config.temperature if self.model_config.do_sample else 1.0
                )
            
            # Çıktıyı decode et
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            
            # Koşullu metni temizle
            if conditional_text:
                caption = caption.replace(conditional_text, "").strip()
            
            return caption.strip()
            
        except Exception as e:
            if isinstance(e, ImageProcessingError):
                raise
            raise GenerationError("Caption generation", str(e))
    
    def generate_title(self, image: Union[str, Image.Image]) -> str:
        """
        Görsel için başlık üret
        
        Args:
            image: Görsel dosyası
            
        Returns:
            str: Üretilen başlık
        """
        try:
            title = self.generate_caption(image, self.analysis_config.title_prompt)
              # Başlığı formatla
            title = title.capitalize()
            if len(title) > self.analysis_config.title_max_length:
                title = title[:self.analysis_config.title_max_length] + "..."
            
            return title if title else "Untitled"
            
        except Exception as e:
            logger.warning(f"Başlık üretme hatası: {str(e)}")
            return "Untitled"
    
    def analyze_image(self, image: Union[str, Image.Image]) -> Dict[str, Any]:
        """
        Görsel için kapsamlı analiz yap
        
        Args:
            image: Görsel dosyası
            
        Returns:
            dict: Analiz sonucu
        """
        try:
            if image is None:
                return {
                    'title': "❌ Görsel yok",
                    'caption': "Lütfen bir görsel yükleyin",
                    'status': "❌ Görsel seçilmedi",
                    'success': False,
                    'image_info': None
                }
            
            # Görsel bilgilerini al (hata durumunda None)
            try:
                image_info = ImageUtils.get_image_info(image)
            except Exception:
                image_info = None
            
            # Başlık üret
            title = self.generate_title(image)
            
            # Açıklama üret
            caption = self.generate_caption(image, self.analysis_config.caption_prompt)
            
            logger.info(f"✅ Analiz tamamlandı - Başlık: {title}")
            
            return {
                'title': title,
                'caption': caption,
                'status': "✅ Analiz tamamlandı!",
                'success': True,
                'image_info': image_info,
                'model_info': {
                    'model_name': self.model_config.model_name,
                    'device': self.device
                }
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Analiz hatası: {error_msg}")
            return {
                'title': "❌ Analiz hatası",
                'caption': f"Hata detayı: {error_msg}",
                'status': "❌ İşlem başarısız",
                'success': False,
                'image_info': None,
                'error': error_msg
            }
    
    def save_image_with_metadata(
        self, 
        image: Union[str, Image.Image], 
        title: str, 
        caption: str,
        output_dir: Optional[str] = None
    ) -> str:
        """
        Görseli metadata ile birlikte kaydet
        
        Args:
            image: Görsel dosyası
            title (str): Başlık
            caption (str): Açıklama
            output_dir (str, optional): Çıktı klasörü
            
        Returns:
            str: İşlem sonucu mesajı
        """
        try:
            if image is None:
                return "❌ Kaydedilecek görsel yok"
            
            # Çıktı klasörünü belirle
            if output_dir is None:
                output_dir = self.analysis_config.output_directory
            
            # Klasörü oluştur
            FileUtils.ensure_directory(output_dir)
            
            # Görseli PIL Image'e çevir
            if isinstance(image, str):
                pil_image = Image.open(image).convert('RGB')
            else:
                pil_image = ImageUtils.preprocess_image(image)
            
            # Dosya adını oluştur
            safe_title = FileUtils.create_safe_filename(title)
            file_path = FileUtils.get_unique_filepath(
                f"{output_dir}/{safe_title}.jpg"
            )
              # Görseli kaydet
            pil_image.save(
                file_path, 
                self.analysis_config.output_format,
                quality=self.analysis_config.image_quality,
                optimize=True
            )
            
            # Metadata kaydet
            if self.analysis_config.save_metadata:
                try:
                    image_info = ImageUtils.get_image_info(pil_image)
                    additional_info = {
                        'Original Size': f"{image_info['width']}x{image_info['height']}",
                        'File Format': image_info['format'],
                        'Device': self.device
                    }
                except Exception:
                    # Image info alınamazsa basit bilgi kaydet
                    additional_info = {
                        'Device': self.device,
                        'Processing': 'Successful'
                    }
                
                FileUtils.save_metadata(
                    file_path, 
                    title, 
                    caption, 
                    self.model_config.model_name,
                    additional_info
                )
            
            logger.info(f"💾 Görsel kaydedildi: {file_path}")
            return f"✅ Görsel kaydedildi: {file_path}"
            
        except Exception as e:
            error_msg = f"Kaydetme hatası: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return f"❌ {error_msg}"
    
    def batch_analyze(
        self, 
        image_paths: List[str],
        save_results: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Birden fazla görseli toplu analiz et
        
        Args:
            image_paths (List[str]): Görsel dosya yolları
            save_results (bool): Sonuçları kaydet
            
        Returns:
            List[dict]: Analiz sonuçları
        """
        results = []
        
        # İlerleme takibi
        if self.analysis_config.show_progress:
            progress = ProgressTracker(len(image_paths), "Görsel Analizi")
        
        for i, image_path in enumerate(image_paths):
            try:
                # Analiz yap
                result = self.analyze_image(image_path)
                result['file_path'] = image_path
                
                # Kaydetme
                if save_results and result['success']:
                    save_result = self.save_image_with_metadata(
                        image_path,
                        result['title'],
                        result['caption']
                    )
                    result['save_result'] = save_result
                
                results.append(result)
                
                # İlerleme güncelle
                if self.analysis_config.show_progress:
                    progress.update()
                
            except Exception as e:
                error_result = {
                    'file_path': image_path,
                    'title': "❌ Hata",
                    'caption': str(e),
                    'status': "❌ Başarısız",
                    'success': False,
                    'error': str(e)
                }
                results.append(error_result)
                
                logger.error(f"❌ Hata: {image_path} - {str(e)}")
                
                if self.analysis_config.show_progress:
                    progress.update()
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Model bilgilerini al
        
        Returns:
            dict: Model bilgileri
        """
        return {
            'model_name': self.model_config.model_name,
            'device': self.device,
            'cuda_available': torch.cuda.is_available(),
            'model_config': self.model_config.to_dict(),
            'analysis_config': self.analysis_config.to_dict()
        }

# Geriye uyumluluk için eski sınıf adı
ImageAnalyzer_Legacy = ImageAnalyzer