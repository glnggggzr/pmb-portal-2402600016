# Portal PMB — Praktikum Cloud Computing P06

Nama: Gilang Zahra Ramdhani  
NIM: 2402600016

Aplikasi Flask mengikuti Modul Praktikum Pertemuan 6 dan contoh demonstrasi dosen. Halaman utama berupa HTML sederhana dengan identitas mahasiswa. Informasi JSON dari contoh modul tersedia di `/api/info`.

## Endpoint

- `GET /`: halaman HTML dengan nama, NIM, Health Check, dan API Info.
- `GET /api/info`: informasi layanan, identitas, versi, gelombang, lingkungan, region, commit, instance, penghitung permintaan, dan waktu UTC.
- `GET /health`: `{"status":"ok"}`.

## Menjalankan lokal

Gunakan Python 3.13.

```sh
python -m venv .venv
# Aktifkan virtual environment sesuai sistem operasi.
python -m pip install -r requirements.txt
python app.py
```

Akses `http://localhost:8000`. Uji otomatis: `python -m unittest -v`.

## Deployment Vercel

Import repositori ini sebagai project `pmb-portal-2402600016` pada paket Hobby. Gunakan entrypoint `app.py` dan Python 3.13 dari `.python-version`.

Atur environment variables sebelum deploy:

| Variabel | Nilai |
| --- | --- |
| `APP_VERSION` | `v1` |
| `PMB_GELOMBANG` | `Gelombang 1` |

Setelah deployment selesai, uji domain production, `/health`, dan `/api/info`. Pertahankan project sampai selesai dinilai. Jangan memasukkan kredensial ke repositori.

## GitHub Actions

Workflow `.github/workflows/deploy.yml` menguji aplikasi dengan Python 3.13. Push ke `main` atau pemicu manual menjalankan deployment production setelah tes lulus; pull request hanya menjalankan tes.

Deployment memerlukan repository secret `VERCEL_TOKEN` yang valid untuk project ini. Token tidak boleh ditaruh dalam kode. Perbarui secret sebelum token kedaluwarsa. ID project dan organisasi pada workflow bukan token rahasia.

Workflow mengisi `CI_GIT_SHA`, `CI_RUN_ID`, dan `DEPLOYED_BY_GITHUB_ACTIONS` pada deployment. Halaman hanya menampilkan keterangan GitHub Actions ketika deployment membawa penanda tersebut, beserta tautan ke run yang bersangkutan. Tahap verifikasi memeriksa endpoint publik dan kecocokan commit.

Jalankan `python scripts/verify_deployment.py` untuk memeriksa aplikasi publik. Untuk memverifikasi deployment CI tertentu, isi environment variable `EXPECTED_COMMIT` dengan SHA commit yang diharapkan.

## Catatan pengamatan

`id_instance` dan `permintaan_ke` berada dalam memori proses untuk latihan stateless. Penghitung ini bukan basis data dan tidak boleh digunakan sebagai jumlah pendaftar sebenarnya.
