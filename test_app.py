import importlib.util
import unittest


class PortalTests(unittest.TestCase):
    def test_portal_returns_module_fields(self):
        self.assertIsNotNone(importlib.util.find_spec('app'), 'Aplikasi Flask belum dibuat')
        from app import app
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['layanan'], 'Portal PMB Universitas Teknologi Muhammadiyah')
        self.assertEqual(data['versi'], 'v1')
        for key in ['gelombang', 'lingkungan', 'region', 'commit', 'id_instance', 'permintaan_ke', 'waktu_utc']:
            self.assertIn(key, data)
    def test_health_is_ok(self):
        from app import app
        response = app.test_client().get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'status': 'ok'})


if __name__ == '__main__':
    unittest.main()
