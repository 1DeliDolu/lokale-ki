#!/usr/bin/env python3
"""
Komut Satırı Görsel Analizi
Terminal'den direkt görsel analizi yapmak için kullanın.
"""

from image_analysis import ImageAnalyzer, analyze_image, batch_analyze_folder
import sys
import os
import glob
import argparse

def analyze_single_image(image_path, save_result=False):
    """
    Tek bir görseli analiz et
    """
    analyzer = ImageAnalyzer()
    
    if not os.path.exists(image_path):
        print(f"❌ Dosya bulunamadı: {image_path}")
        return False
    
    print(f"📸 Analiz ediliyor: {os.path.basename(image_path)}")
    
    # Analiz yap
    result = analyzer.analyze_image(image_path)
    
    # Sonuçları yazdır
    print("\n" + "="*50)
    print(f"📝 Başlık: {result['title']}")
    print(f"🔍 Açıklama: {result['caption']}")
    print(f"📊 Durum: {result['status']}")
    print("="*50)
    
    # Kaydet
    if save_result and result['success']:
        save_result = analyzer.save_image_with_metadata(
            image_path, result['title'], result['caption']
        )
        print(f"💾 {save_result}")
    
    return result['success']

def analyze_folder(folder_path, save_results=False):
    """
    Klasördeki tüm görselleri analiz et
    """
    # Desteklenen formatlar
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
        image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    if not image_files:
        print(f"❌ {folder_path} klasöründe görsel dosyası bulunamadı")
        return False
    
    print(f"📁 {len(image_files)} görsel bulundu")
    
    # Analyzer oluştur
    analyzer = ImageAnalyzer()
    
    # Toplu analiz
    results = analyzer.batch_analyze(image_files)
    
    # Sonuçları özetle
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"\n📊 Analiz Özeti:")
    print(f"✅ Başarılı: {successful}")
    print(f"❌ Başarısız: {failed}")
    
    # Kaydetme
    if save_results:
        print("\n💾 Sonuçlar kaydediliyor...")
        for result in results:
            if result['success']:
                analyzer.save_image_with_metadata(
                    result['file_path'],
                    result['title'], 
                    result['caption']
                )
        print("✅ Tüm sonuçlar kaydedildi!")
    
    return True

def main():
    """
    Komut satırı arayüzü
    """
    parser = argparse.ArgumentParser(
        description="AI Görsel Açıklayıcı - Komut Satırı Versiyonu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python cli_analyzer.py image.jpg                    # Tek görsel analizi
  python cli_analyzer.py image.jpg --save             # Analiz et ve kaydet
  python cli_analyzer.py --folder ./images            # Klasör analizi
  python cli_analyzer.py --folder ./images --save     # Klasör analizi + kaydetme
        """
    )
    
    parser.add_argument('image', nargs='?', help='Analiz edilecek görsel dosyası')
    parser.add_argument('--folder', '-f', help='Analiz edilecek klasör')
    parser.add_argument('--save', '-s', action='store_true', help='Sonuçları kaydet')
    
    args = parser.parse_args()
    
    # Hiçbir argüman verilmemişse help göster
    if not args.image and not args.folder:
        parser.print_help()
        return
    
    print("🤖 AI Görsel Açıklayıcı - CLI")
    print("="*40)
    
    success = False
    
    if args.folder:
        # Klasör analizi
        success = analyze_folder(args.folder, args.save)
    elif args.image:
        # Tek görsel analizi
        success = analyze_single_image(args.image, args.save)
    
    if success:
        print("\n✅ İşlem tamamlandı!")
    else:
        print("\n❌ İşlem başarısız!")
        sys.exit(1)

if __name__ == "__main__":
    main()