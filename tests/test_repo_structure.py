import unittest
import json
import os

class TestRepoStructure(unittest.TestCase):
    """Test repository structure, JSON validity, and manifest links."""
    
    def setUp(self):
        self.repo_root = os.path.dirname(os.path.abspath(__file__)) + '/..'
        self.repo_root = os.path.normpath(self.repo_root)
    
    def test_plugins_json_valid(self):
        """plugins.json must be valid JSON array."""
        path = os.path.join(self.repo_root, 'plugins.json')
        with open(path, 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
    
    def test_repo_json_valid(self):
        """repo.json must be valid JSON object with required fields."""
        path = os.path.join(self.repo_root, 'repo.json')
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
        self.assertIn('name', data)
        self.assertIn('description', data)
        self.assertIn('manifestVersion', data)
        self.assertIn('pluginLists', data)
    
    def test_repo_json_plugin_url_correct(self):
        """repo.json pluginLists must point to correct plugins.json URL."""
        path = os.path.join(self.repo_root, 'repo.json')
        with open(path, 'r') as f:
            data = json.load(f)
        
        expected_url = "https://raw.githubusercontent.com/BobMmarleyy/turkstream-repo/builds/plugins.json"
        self.assertEqual(data['pluginLists'][0], expected_url)
    
    def test_sources_json_valid(self):
        """sources.json must be valid JSON with sources array."""
        path = os.path.join(self.repo_root, 'sources.json')
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, dict)
        self.assertIn('sources', data)
        self.assertIsInstance(data['sources'], list)
    
    def test_sources_have_required_fields(self):
        """Each source must have name, url, type, and timeout."""
        path = os.path.join(self.repo_root, 'sources.json')
        with open(path, 'r') as f:
            data = json.load(f)
        
        for source in data['sources']:
            self.assertIn('name', source)
            self.assertIn('url', source)
            self.assertIn('type', source)
            self.assertIn('timeout', source)

if __name__ == '__main__':
    unittest.main()