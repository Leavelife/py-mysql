# Sistem Monitoring Tugas Akhir

Proyek ini merupakan aplikasi sistem monitoring tugas akhir mahasiswa menggunakan **MySQL** sebagai database, **Flask (Python)** untuk backend API, dan **Tkinter (Python)** untuk frontend GUI.

---

## 📋 Software dan Tools yang Dibutuhkan

| Komponen        | Versi Disarankan    | Keterangan                      |
|-----------------|--------------------|--------------------------------|
| Python          | 3.8+               | Bahasa pemrograman utama        |
| MySQL Server    | 8.x                | Database server                 |
| phpMyAdmin      | Terpasang opsional  | Untuk manajemen MySQL secara GUI |
| Git             | Terpasang opsional  | Version control                 |
| Editor/IDE      | VSCode / PyCharm   | Untuk coding                   |
| Postman         | Terpasang opsional  | Untuk testing API               |

---

## 📦 Library Python yang Digunakan

- **Backend (Flask API)**
  - `flask`
  - `mysql-connector-python`
  - `python-dotenv`

- **Frontend (Tkinter GUI)**
  - `tkinter` (bawaan Python)
  - `requests` (untuk request ke API)

---

## ⚙️ Setup Database

1. Install MySQL Server dan phpMyAdmin (opsional).
2. Impor file .sql yang terlampir ke phpMyAdmin:

## 🏗️ Setup Backend (Flask)
1. Buat virtual environment (disarankan):
```json
python -m venv venv
source venv/bin/activate    # Linux / MacOS
venv\Scripts\activate       # Windows
```
2. Buat file requirement.txt dan insttal dependencies
```json
pip install -r requirements.txt
```
3. Ubah setup di file db.py
4. Jalankan app.py

## 🖥️ Setup Frontend (Tkinter)
1. Pastikan Python sudah terinstall dengan modul tkinter dan requests.
2. Jalankan script frontend.py
3. GUI akan muncul, dan secara otomatis akan mengambil data dari API backend.

## 📌 Testing API
Gunakan Postman atau curl untuk testing API, misalnya:

1. GET daftar monitoring tugas:
```json
GET http://localhost:5000/monitoring/list
```