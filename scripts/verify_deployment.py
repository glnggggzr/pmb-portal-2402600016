import json
import os
import time
import urllib.error
import urllib.request

BASE_URL = 'https://pmb-portal-2402600016.vercel.app'
expected_commit = os.environ.get('EXPECTED_COMMIT', '')[:7]

for attempt in range(12):
    try:
        with urllib.request.urlopen(BASE_URL, timeout=20) as response:
            assert response.status == 200
            html = response.read().decode()
            assert 'Flask App with CI/CD Test, NIM: 2402600016' in html
            assert 'href="/health"' in html and 'href="/api/info"' in html
            if expected_commit:
                assert 'Deployed automatically using GitHub Actions' in html
        with urllib.request.urlopen(BASE_URL + '/health', timeout=20) as response:
            assert response.status == 200
            assert json.load(response) == {'status': 'ok'}
        with urllib.request.urlopen(BASE_URL + '/api/info', timeout=20) as response:
            assert response.status == 200
            data = json.load(response)
            assert data['nim'] == '2402600016'
            assert data['lingkungan'] == 'production'
            if expected_commit:
                assert data['commit'] == expected_commit
        print('PASS: public homepage, identity, navigation, health, API and commit.')
        break
    except (AssertionError, urllib.error.URLError, TimeoutError) as error:
        if attempt == 11:
            raise
        print('Waiting for the expected deployment to become publicly available.')
        time.sleep(5)
