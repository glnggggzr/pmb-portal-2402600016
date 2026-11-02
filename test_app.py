import importlib.util
import unittest


class PortalTests(unittest.TestCase):
    def test_portal_returns_module_fields(self):
        self.assertIsNotNone(importlib.util.find_spec('app'), 'Aplikasi Flask belum dibuat')
        from app import app
        response = app.test_client().get('/api/info')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['layanan'], 'Portal PMB Universitas Teknologi Muhammadiyah')
        self.assertEqual(data['versi'], 'v1')
        for key in ['gelombang', 'lingkungan', 'region', 'commit', 'id_instance', 'permintaan_ke', 'waktu_utc']:
            self.assertIn(key, data)
    def test_homepage_has_identity_and_working_links(self):
        from app import app
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/html')
        html = response.get_data(as_text=True)
        self.assertIn('Flask App with CI/CD Test, NIM: 2402600016', html)
        self.assertIn('Gilang Zahra Ramdhani', html)
        for target in ['/health', '/api/info']:
            self.assertIn(f'href="{target}"', html)
            self.assertEqual(app.test_client().get(target).status_code, 200)
        self.assertNotIn('Deployed automatically using GitHub Actions', html)

    def test_ci_deployment_links_to_actual_run(self):
        import os
        from unittest.mock import patch
        from app import app
        with patch.dict(os.environ, {'DEPLOYED_BY_GITHUB_ACTIONS': 'true', 'CI_RUN_ID': '12345', 'CI_GIT_SHA': 'abcdef1234567890'}):
            html = app.test_client().get('/').get_data(as_text=True)
            self.assertIn('Deployed automatically using GitHub Actions', html)
            self.assertIn('https://github.com/glnggggzr/pmb-portal-2402600016/actions/runs/12345', html)
            data = app.test_client().get('/api/info').get_json()
            self.assertEqual(data['commit'], 'abcdef1')
            self.assertEqual(data['nim'], '2402600016')
            self.assertEqual(data['nama'], 'Gilang Zahra Ramdhani')

    def test_health_is_ok(self):
        from app import app
        response = app.test_client().get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'status': 'ok'})


if __name__ == '__main__':
    unittest.main()
