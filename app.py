import os
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

# Dibuat sekali per instance fungsi untuk pengamatan stateless pada modul.
ID_INSTANCE = uuid.uuid4().hex[:8]
jumlah_permintaan = 0


@app.route('/')
def beranda():
    global jumlah_permintaan
    jumlah_permintaan += 1
    commit = os.environ.get('VERCEL_GIT_COMMIT_SHA', 'lokal')[:7]
    return jsonify(
        layanan='Portal PMB Universitas Teknologi Muhammadiyah',
        versi=os.environ.get('APP_VERSION', 'v1'),
        gelombang=os.environ.get('PMB_GELOMBANG', 'belum diatur'),
        lingkungan=os.environ.get('VERCEL_ENV', 'lokal'),
        region=os.environ.get('VERCEL_REGION', 'tidak diketahui'),
        commit=commit,
        id_instance=ID_INSTANCE,
        permintaan_ke=jumlah_permintaan,
        waktu_utc=datetime.now(timezone.utc).isoformat(),
    )


@app.route('/health')
def health():
    return jsonify(status='ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
