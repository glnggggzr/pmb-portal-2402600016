# Portal PMB — Praktikum Cloud Computing P06

Nama: Gilang Zahra Ramdhani  
NIM: 2402600016

Aplikasi Flask mengikuti bagian 7.1–7.2 Modul Praktikum Pertemuan 6. Respons utama berupa JSON, sesuai contoh modul.

## Endpoint

- `GET /`: informasi layanan, versi, gelombang, lingkungan, region, commit, instance, penghitung permintaan, dan waktu UTC.
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

Setelah deployment selesai, uji domain production dan endpoint `/health`. Pertahankan project sampai selesai dinilai. Jangan memasukkan kredensial ke repositori.

## Catatan pengamatan

`id_instance` dan `permintaan_ke` berada dalam memori proses untuk latihan stateless. Penghitung ini bukan basis data dan tidak boleh digunakan sebagai jumlah pendaftar sebenarnya.
