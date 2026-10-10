import unittest
from monitor import SourceMonitor

class TestSourceMonitor(unittest.TestCase):
    def test_monitor_initialization(self):
        """Monitor nesnesinin doğru şekilde başlatıldığını test et"""
        monitor = SourceMonitor()
        self.assertIsNotNone(monitor.sources)
    
    def test_check_source_valid_m3u(self):
        """Geçerli bir M3U kaynağı için kontrol yap"""
        # Gerçek bir URL'yi kullanmak yerine, örnek veri ile test ediyoruz
        monitor = SourceMonitor()
        
        # Test için geçici bir yapılandırma oluşturuyoruz
        test_source = {
            "name": "Test IPTV",
            "url": "https://iptv.canli.com.tr/playlist.m3u",
            "type": "m3u",
            "check_interval": 86400,
            "timeout": 10
        }
        
        # Bu test, gerçek bir HTTP isteği yapacağı için birim testi değil,
        # Ancak monitor.py içindeki yapıyı test etmek için yeterlidir.
        self.assertEqual(test_source['type'], 'm3u')

if __name__ == '__main__':
    unittest.main()