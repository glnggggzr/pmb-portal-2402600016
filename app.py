import os
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Dibuat sekali per instance fungsi untuk pengamatan stateless pada modul.
ID_INSTANCE = uuid.uuid4().hex[:8]
jumlah_permintaan = 0


@app.route('/')
def beranda():
    run_id = os.environ.get('CI_RUN_ID', '')
    automated = os.environ.get('DEPLOYED_BY_GITHUB_ACTIONS') == 'true' and run_id.isdecimal()
    return render_template('index.html', automated=automated, run_id=run_id)


@app.route('/api/info')
def info():
    global jumlah_permintaan
    jumlah_permintaan += 1
    commit = os.environ.get('CI_GIT_SHA') or os.environ.get('VERCEL_GIT_COMMIT_SHA', 'lokal')
    return jsonify(
        layanan='Portal PMB Universitas Teknologi Muhammadiyah',
        versi=os.environ.get('APP_VERSION', 'v1'),
        gelombang=os.environ.get('PMB_GELOMBANG', 'belum diatur'),
        lingkungan=os.environ.get('VERCEL_ENV', 'lokal'),
        region=os.environ.get('VERCEL_REGION', 'tidak diketahui'),
        commit=commit[:7],
        nama='Gilang Zahra Ramdhani',
        nim='2402600016',
        id_instance=ID_INSTANCE,
        permintaan_ke=jumlah_permintaan,
        waktu_utc=datetime.now(timezone.utc).isoformat(),
    )


@app.route('/health')
def health():
    return jsonify(status='ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
