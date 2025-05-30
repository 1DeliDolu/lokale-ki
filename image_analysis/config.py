"""
Konfigürasyon sınıfları - Model ve analiz ayarları
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class ModelConfig:
    """
    Model konfigürasyonu
    """
    model_name: str = "Salesforce/blip-image-captioning-base"
    device: str = "auto"  # "auto", "cpu", "cuda"
    cache_dir: Optional[str] = None
    torch_dtype: str = "float32"
    use_auth_token: Optional[str] = None
    
    # Generation parametreleri
    max_length: int = 50
    num_beams: int = 2
    do_sample: bool = False
    early_stopping: bool = True
    temperature: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük olarak döndür"""
        return {
            'model_name': self.model_name,
            'device': self.device,
            'cache_dir': self.cache_dir,
            'torch_dtype': self.torch_dtype,
            'use_auth_token': self.use_auth_token,
            'max_length': self.max_length,
            'num_beams': self.num_beams,
            'do_sample': self.do_sample,
            'early_stopping': self.early_stopping,
            'temperature': self.temperature
        }

@dataclass
class AnalysisConfig:
    """
    Analiz konfigürasyonu
    """
    max_image_size: int = 512
    image_quality: int = 95
    output_format: str = "JPEG"
    
    # Başlık ayarları
    title_max_length: int = 50
    title_prompt: str = "a photo of"
    
    # Açıklama ayarları
    caption_prompt: str = ""
    
    # Kaydetme ayarları
    save_metadata: bool = True
    output_directory: str = "captioned_images"
    
    # Batch işleme
    batch_size: int = 1
    show_progress: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük olarak döndür"""
        return {
            'max_image_size': self.max_image_size,
            'image_quality': self.image_quality,
            'output_format': self.output_format,
            'title_max_length': self.title_max_length,
            'title_prompt': self.title_prompt,
            'caption_prompt': self.caption_prompt,
            'save_metadata': self.save_metadata,
            'output_directory': self.output_directory,
            'batch_size': self.batch_size,
            'show_progress': self.show_progress
        }

# Önceden tanımlı konfigürasyonlar
class PresetConfigs:
    """
    Hazır konfigürasyonlar
    """
    
    @staticmethod
    def fast_config() -> tuple[ModelConfig, AnalysisConfig]:
        """Hızlı analiz için konfigürasyon"""
        model_config = ModelConfig(
            model_name="Salesforce/blip-image-captioning-base",
            max_length=30,
            num_beams=1
        )
        
        analysis_config = AnalysisConfig(
            max_image_size=256,
            image_quality=85
        )
        
        return model_config, analysis_config
    
    @staticmethod
    def quality_config() -> tuple[ModelConfig, AnalysisConfig]:
        """Yüksek kalite analiz için konfigürasyon"""
        model_config = ModelConfig(
            model_name="Salesforce/blip2-opt-2.7b",
            max_length=100,
            num_beams=5,
            do_sample=True,
            temperature=0.7
        )
        
        analysis_config = AnalysisConfig(
            max_image_size=1024,
            image_quality=95
        )
        
        return model_config, analysis_config
    
    @staticmethod
    def batch_config() -> tuple[ModelConfig, AnalysisConfig]:
        """Toplu işlem için konfigürasyon"""
        model_config = ModelConfig(
            model_name="Salesforce/blip-image-captioning-base",
            max_length=40,
            num_beams=2
        )
        
        analysis_config = AnalysisConfig(
            max_image_size=512,
            batch_size=4,
            show_progress=True
        )
        
        return model_config, analysis_config