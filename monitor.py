import requests
import json
import time
from datetime import datetime
import logging

# Log ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SourceMonitor:
    def __init__(self, config_file='sources.json'):
        try:
            with open(config_file) as f:
                self.sources = json.load(f)['sources']
            logger.info(f"Yüklenen kaynak sayısı: {len(self.sources)}")
        except Exception as e:
            logger.error(f"Kaynak dosyası okunurken hata oluştu: {e}")
            self.sources = []
    
    def check_source(self, source):
        """Kaynak erişilebilirliğini kontrol et"""
        try:
            # Gerekli alanların varlığını doğrula
            if not all(key in source for key in ['url', 'type', 'timeout']):
                return False, f"Geçersiz yapılandırma: {source}"
            
            logger.info(f"{source['name']} kaynağı kontrol ediliyor...")
            
            response = requests.get(source['url'], timeout=source['timeout'])
            if response.status_code == 200:
                # HTTP durumu iyiysa, içerik türünü de doğrula
                content_type = response.headers.get('content-type', '')
                
                logger.info(f"{source['name']} - İçerik türü: {content_type}")
                
                if source['type'] == 'm3u' and ('application/x-mpegURL' in content_type or 'audio/mpegurl' in content_type):
                    return True, "M3U dosyası doğru şekilde sunuluyor"
                elif source['type'] == 'xml' and 'text/xml' in content_type:
                    return True, "XML dosyası doğru şekilde sunuluyor"
                else:
                    # İçerik doğrulaması için basit içerik kontrolü
                    if source['type'] == 'm3u' and response.text.startswith('#EXTINF:'):
                        return True, "M3U listesi geçerli"
                    elif source['type'] == 'xml' and '<xml' in response.text.lower():
                        return True, "XML dosyası geçerli"
                return False, f"İçerik türü beklenen formatta değil: {content_type}"
            else:
                return False, f"HTTP hata kodu: {response.status_code} - {response.reason}"
        except requests.exceptions.Timeout:
            logger.error(f"{source['name']} için zaman aşımı oluştu")
            return False, "Zaman aşımı oluştu"
        except requests.exceptions.ConnectionError:
            logger.error(f"{source['name']} için bağlantı hatası")
            return False, "Bağlantı hatası"
        except requests.exceptions.RequestException as e:
            logger.error(f"{source['name']} için istek hatası: {e}")
            return False, f"İstek hatası: {str(e)}"
        except Exception as e:
            logger.error(f"{source['name']} için beklenmeyen hata: {e}")
            return False, f"Hata oluştu: {str(e)}"
    
    def monitor_all(self):
        """Tüm kaynakları kontrol et"""
        results = []
        failed_sources = 0
        
        for source in self.sources:
            status, message = self.check_source(source)
            if not status:
                failed_sources += 1
            results.append({
                'name': source['name'],
                'url': source['url'],
                'status': status,
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
        
        # Sonuçları logla
        with open('monitor_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Toplam {len(self.sources)} kaynak kontrol edildi. {failed_sources} hatalı.")
        
        return results

if __name__ == "__main__":
    monitor = SourceMonitor()
    
    # Kontrolleri başlat
    results = monitor.monitor_all()
    
    print("Kaynak Kontrol Sonuçları:")
    for result in results:
        status_icon = "✅" if result['status'] else "❌"
        print(f"{status_icon} {result['name']} - {result['message']}")
    
    # Hatalı kaynak varsa programı hata koduyla sonlandır
    failed_count = sum(1 for r in results if not r['status'])
    if failed_count > 0:
        print(f"\n{failed_count} adet kaynak başarısız!")
        exit(1)