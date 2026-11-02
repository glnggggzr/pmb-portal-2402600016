import importlib.util
import json
from pathlib import Path
import unittest


class DeploymentTests(unittest.TestCase):
    def test_payload_has_only_app_files_and_public_build_identity(self):
        self.assertIsNotNone(importlib.util.find_spec('scripts.deploy_vercel'), 'Deployment API belum dibuat')
        from scripts.deploy_vercel import build_payload
        root = Path(__file__).parent
        payload = build_payload(root, 'abcdef1234567890', '12345')
        self.assertEqual(payload['project'], 'prj_EVfanJYgwg5tLJQsAKiwm93SeQ13')
        self.assertEqual(payload['target'], 'production')
        files = {item['file']: item for item in payload['files']}
        self.assertEqual(set(files), {'app.py', 'requirements.txt', '.python-version', 'templates/index.html', 'deployment_info.json'})
        metadata = json.loads(files['deployment_info.json']['data'])
        self.assertEqual(metadata, {'source': 'github-actions', 'run_id': '12345', 'commit': 'abcdef1234567890'})
        self.assertNotIn('VERCEL_TOKEN', json.dumps(payload))
