"""
AI Görsel Analiz Modülü

Bu modül, yapay zeka kullanarak görselleri analiz etmek ve açıklama üretmek 
için gerekli tüm araçları sağlar.

Kullanım:
    from image_analysis import ImageAnalyzer
    
    analyzer = ImageAnalyzer()
    result = analyzer.analyze_image("image.jpg")
"""

from .analyzer import ImageAnalyzer
from .config import ModelConfig, AnalysisConfig, PresetConfigs
from .utils import ImageUtils, FileUtils
from .exceptions import ImageAnalysisError, ModelLoadError

__version__ = "1.0.0"
__author__ = "AI Development Team"
__email__ = "mustafa.ozdemir1408@gmail.com"

# Ana sınıfları dışa aktar
__all__ = [
    'ImageAnalyzer',
    'ModelConfig', 
    'AnalysisConfig',
    'PresetConfigs',
    'ImageUtils',
    'FileUtils',
    'ImageAnalysisError',
    'ModelLoadError'
]

# Modül seviyesinde kolaylık fonksiyonları
def analyze_image(image_path, model_name=None):
    """
    Hızlı görsel analizi
    
    Args:
        image_path (str): Görsel dosya yolu
        model_name (str, optional): Kullanılacak model adı
    
    Returns:
        dict: Analiz sonucu
    """
    analyzer = ImageAnalyzer(model_name=model_name)
    return analyzer.analyze_image(image_path)

def batch_analyze_folder(folder_path, model_name=None, save_results=False):
    """
    Klasördeki tüm görselleri analiz et
    
    Args:
        folder_path (str): Klasör yolu
        model_name (str, optional): Model adı
        save_results (bool): Sonuçları kaydet
    
    Returns:
        list: Analiz sonuçları
    """
    analyzer = ImageAnalyzer(model_name=model_name)
    
    # Klasördeki görselleri bul
    from pathlib import Path
    import glob
    
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(str(Path(folder_path) / ext)))
        image_files.extend(glob.glob(str(Path(folder_path) / ext.upper())))
    
    # Toplu analiz
    results = analyzer.batch_analyze(image_files)
    
    # Kaydetme
    if save_results:
        for result in results:
            if result['success']:
                analyzer.save_image_with_metadata(
                    result['file_path'],
                    result['title'],
                    result['caption']
                )
    
    return results