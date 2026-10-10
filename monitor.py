import requests
import json
import time
from datetime import datetime

class SourceMonitor:
    def __init__(self, config_file='sources.json'):
        with open(config_file) as f:
            self.sources = json.load(f)['sources']
    
    def check_source(self, source):
        """Kaynak erişilebilirliğini kontrol et"""
        try:
            response = requests.get(source['url'], timeout=source['timeout'])
            if response.status_code == 200:
                # HTTP durumu iyiysa, içerik türünü de doğrula
                content_type = response.headers.get('content-type', '')
                if source['type'] == 'm3u' and 'application/x-mpegURL' in content_type:
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
                return False, f"HTTP hata kodu: {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "Zaman aşımı oluştu"
        except Exception as e:
            return False, f"Hata oluştu: {str(e)}"
    
    def monitor_all(self):
        """Tüm kaynakları kontrol et"""
        results = []
        for source in self.sources:
            status, message = self.check_source(source)
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
        
        return results

if __name__ == "__main__":
    monitor = SourceMonitor()
    results = monitor.monitor_all()
    
    print("Kaynak Kontrol Sonuçları:")
    for result in results:
        status_icon = "✅" if result['status'] else "❌"
        print(f"{status_icon} {result['name']} - {result['message']}")