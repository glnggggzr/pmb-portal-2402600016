import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.request

PROJECT_ID = 'prj_EVfanJYgwg5tLJQsAKiwm93SeQ13'
TEAM_ID = 'team_Wtlvhx0je7OcV613fM7nd1KE'
APP_FILES = ('app.py', 'requirements.txt', '.python-version', 'templates/index.html')


def build_payload(root, commit, run_id):
    files = [{'file': name, 'data': (root / name).read_text(encoding='utf-8'), 'encoding': 'utf-8'} for name in APP_FILES]
    metadata = {'source': 'github-actions', 'run_id': run_id, 'commit': commit}
    files.append({'file': 'deployment_info.json', 'data': json.dumps(metadata), 'encoding': 'utf-8'})
    return {
        'name': 'pmb-portal-2402600016',
        'project': PROJECT_ID,
        'target': 'production',
        'files': files,
        'projectSettings': {'framework': 'flask'},
        'gitMetadata': {
            'remoteUrl': 'https://github.com/glnggggzr/pmb-portal-2402600016',
            'commitSha': commit,
            'commitRef': 'main',
            'ci': True,
            'ciType': 'github-actions',
            'dirty': False,
        },
    }


def api(path, token, data=None):
    url = 'https://api.vercel.com' + path + '?teamId=' + TEAM_ID
    request = urllib.request.Request(url, headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }, data=None if data is None else json.dumps(data).encode())
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = json.loads(error.read()).get('error', {})
        raise RuntimeError(f"Vercel HTTP {error.code}: {detail.get('code', 'unknown')}: {detail.get('message', '')}") from None


def main():
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise RuntimeError('Jalankan deployment ini dari GitHub Actions.')
    token = os.environ['VERCEL_TOKEN']
    payload = build_payload(Path(__file__).resolve().parent.parent, os.environ['GITHUB_SHA'], os.environ['GITHUB_RUN_ID'])
    deployment = api('/v13/deployments', token, payload)
    deployment_id = deployment['id']
    print('Deployment created:', deployment_id, flush=True)
    for _ in range(90):
        current = api('/v13/deployments/' + deployment_id, token)
        state = current.get('readyState', current.get('status'))
        print('Deployment status:', state, flush=True)
        if state == 'READY':
            print('Ready:', current['url'])
            return
        if state in {'ERROR', 'CANCELED'}:
            raise RuntimeError(f"Deployment {state}: {current.get('errorMessage', '')}")
        time.sleep(5)
    raise TimeoutError('Deployment tidak selesai dalam batas waktu.')


if __name__ == '__main__':
    main()
