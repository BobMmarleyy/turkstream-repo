import unittest
from unittest.mock import patch, Mock
import json
import sys
import os

# monitor.py dosyasını içe aktar
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from monitor import SourceMonitor

class TestSourceMonitor(unittest.TestCase):
    def setUp(self):
        # Test için örnek yapılandırma
        self.test_config = {
            "sources": [
                {
                    "name": "Test M3U",
                    "url": "https://example.com/test.m3u",
                    "type": "m3u",
                    "check_interval": 86400,
                    "timeout": 10
                },
                {
                    "name": "Test XML", 
                    "url": "https://example.com/test.xml",
                    "type": "xml",
                    "check_interval": 86400,
                    "timeout": 10
                }
            ]
        }
        
    @patch('monitor.requests.get')
    def test_check_source_success(self, mock_get):
        # Mock HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'application/x-mpegURL'}
        mock_response.text = "#EXTINF:0 tvg-id=\"test\" group-title=\"Test\",Test\nhttp://example.com/test"
        mock_get.return_value = mock_response
        
        # Testi başlat
        monitor = SourceMonitor()
        status, message = monitor.check_source(self.test_config['sources'][0])
        
        self.assertTrue(status)
        self.assertEqual(message, "M3U dosyası doğru şekilde sunuluyor")
    
    @patch('monitor.requests.get')
    def test_check_source_xml_success(self, mock_get):
        # Mock XML response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'text/xml'}
        mock_response.text = "<?xml version='1.0' encoding='UTF-8'?><root></root>"
        mock_get.return_value = mock_response
        
        monitor = SourceMonitor()
        status, message = monitor.check_source(self.test_config['sources'][1])
        
        self.assertTrue(status)
        self.assertEqual(message, "XML dosyası doğru şekilde sunuluyor")
    
    @patch('monitor.requests.get')
    def test_check_source_failure(self, mock_get):
        # Mock HTTP response with error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.reason = 'Not Found'
        mock_get.return_value = mock_response
        
        monitor = SourceMonitor()
        status, message = monitor.check_source(self.test_config['sources'][0])
        
        self.assertFalse(status)
        self.assertIn("HTTP hata kodu", message)
    
    @patch('monitor.requests.get')
    def test_check_source_timeout(self, mock_get):
        # Mock timeout with correct exception type
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        monitor = SourceMonitor()
        status, message = monitor.check_source(self.test_config['sources'][0])
        
        self.assertFalse(status)
        self.assertEqual(message, "Zaman aşımı oluştu")

if __name__ == '__main__':
    unittest.main()