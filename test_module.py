"""
Örnek kullanım kodları ve testler
"""

from image_analysis import (
    ImageAnalyzer, 
    ModelConfig, 
    AnalysisConfig,
    PresetConfigs,
    analyze_image,
    batch_analyze_folder
)
import os

def test_basic_usage():
    """
    Temel kullanım örneği
    """
    print("🧪 Temel Kullanım Testi")
    print("=" * 40)
    
    # Basit kullanım
    if os.path.exists("test_image.jpg"):
        result = analyze_image("test_image.jpg")
        print(f"Başlık: {result['title']}")
        print(f"Açıklama: {result['caption']}")
    else:
        print("Test görseli bulunamadı")

def test_custom_config():
    """
    Özel konfigürasyon örneği
    """
    print("\n🔧 Özel Konfigürasyon Testi")
    print("=" * 40)
    
    # Özel model konfigürasyonu
    model_config = ModelConfig(
        model_name="Salesforce/blip-image-captioning-base",
        max_length=30,
        num_beams=3
    )
    
    # Özel analiz konfigürasyonu
    analysis_config = AnalysisConfig(
        max_image_size=256,
        title_max_length=30,
        output_directory="custom_output"
    )
    
    # Analyzer oluştur
    analyzer = ImageAnalyzer(model_config, analysis_config)
    
    # Model bilgilerini göster
    info = analyzer.get_model_info()
    print(f"Model: {info['model_name']}")
    print(f"Device: {info['device']}")

def test_preset_configs():
    """
    Hazır konfigürasyonlar testi
    """
    print("\n⚡ Hızlı Konfigürasyon Testi")
    print("=" * 40)
    
    # Hızlı konfigürasyon
    model_config, analysis_config = PresetConfigs.fast_config()
    analyzer = ImageAnalyzer(model_config, analysis_config)
    
    print(f"Hızlı Config - Max Length: {model_config.max_length}")
    print(f"Hızlı Config - Image Size: {analysis_config.max_image_size}")

def test_batch_processing():
    """
    Toplu işlem testi
    """
    print("\n📁 Toplu İşlem Testi")
    print("=" * 40)
    
    # Test klasörü varsa
    test_folder = "test_images"
    if os.path.exists(test_folder):
        results = batch_analyze_folder(test_folder, save_results=True)
        
        successful = sum(1 for r in results if r.get('success', False))
        print(f"✅ Başarılı: {successful}/{len(results)}")
    else:
        print("Test klasörü bulunamadı")

def test_error_handling():
    """
    Hata yönetimi testi
    """
    print("\n🚨 Hata Yönetimi Testi")
    print("=" * 40)
    
    try:
        # Olmayan dosya
        result = analyze_image("nonexistent.jpg")
        print(f"Hata durumu: {result['status']}")
        
    except Exception as e:
        print(f"Yakalanan hata: {str(e)}")

def main():
    """
    Tüm testleri çalıştır
    """
    print("🧪 Image Analysis Modül Testleri")
    print("=" * 50)
    
    try:
        test_basic_usage()
        test_custom_config()
        test_preset_configs()
        test_batch_processing()
        test_error_handling()
        
        print("\n✅ Tüm testler tamamlandı!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Testler durduruldu")
    except Exception as e:
        print(f"\n❌ Test hatası: {str(e)}")

if __name__ == "__main__":
    main()