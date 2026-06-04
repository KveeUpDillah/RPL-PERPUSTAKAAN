# [INF2183] Praktikum Rekayasa Perangkat Lunak
## Proyek UAS Sistem Informasi Perpustakaan (Pustaka BuKu)

### Deskripsi Proyek
Pustaka BuKu adalah aplikasi sistem informasi perpustakaan berbasis web yang dikembangkan menggunakan framework Django dan database MySQL. Sistem ini dirancang untuk membantu pengelolaan perpustakaan secara terstruktur, meliputi manajemen data buku, anggota, transaksi peminjaman dan pengembalian, serta kontrol akses berbasis peran pengguna (role-based access control). Anggota dapat mendaftar secara mandiri dan meminjam buku langsung melalui sistem, sementara admin bertugas mengelola data dan mencatat pengembalian buku. Sistem juga dilengkapi mekanisme sanksi otomatis bagi anggota yang terlambat mengembalikan buku.

---

### Struktur File

```
RPL-PERPUSTAKAAN/
├── perpustakaan/                        : Root direktori proyek Django
│   ├── manage.py                        : Entry point untuk menjalankan perintah Django
│   ├── requirements.txt                 : Daftar dependensi/library yang dibutuhkan
│   │
│   ├── perpustakaan/                    : Folder konfigurasi utama proyek Django
│   │   ├── __init__.py                  : Menandai folder sebagai package Python
│   │   ├── settings.py                  : Konfigurasi proyek (database, app, middleware)
│   │   ├── urls.py                      : Routing URL tingkat proyek
│   │   ├── asgi.py                      : Konfigurasi ASGI untuk deployment async
│   │   └── wsgi.py                      : Konfigurasi WSGI untuk deployment produksi
│   │
│   └── main/                            : Aplikasi utama sistem perpustakaan
│       ├── __init__.py                  : Menandai folder sebagai package Python
│       ├── admin.py                     : Konfigurasi model pada halaman admin Django
│       ├── apps.py                      : Konfigurasi aplikasi main
│       ├── decorators.py                : Custom decorator untuk kontrol akses role
│       ├── forms.py                     : Definisi form input (buku, anggota, peminjaman, dll)
│       ├── models.py                    : Definisi model database (Anggota, Buku, Peminjaman, dll)
│       ├── urls.py                      : Routing URL tingkat aplikasi
│       ├── views.py                     : Logika tampilan dan pemrosesan request
│       ├── tests.py                     : File pengujian unit aplikasi
│       │
│       ├── migrations/                  : Folder migrasi skema database
│       │   ├── __init__.py
│       │   ├── 0001_initial.py          : Migrasi awal pembuatan tabel dasar
│       │   ├── 0002_add_loginhistory.py : Migrasi penambahan riwayat login
│       │   ├── 0003_contact.py          : Migrasi penambahan data kontak
│       │   ├── 0004_anggota_buku_peminjaman_pengembalian_and_more.py : Migrasi model inti
│       │   ├── 0005_alter_anggota_options_alter_buku_options_and_more.py : Migrasi penyesuaian opsi model
│       │   ├── 0006_aktivitas.py        : Migrasi penambahan log aktivitas
│       │   └── 0007_anggota_sanksi_sampai.py : Migrasi penambahan field sanksi anggota
│       │
│       ├── static/                      : File statis (CSS dan JavaScript)
│       │   ├── css/
│       │   │   ├── auth.css             : Styling halaman login dan registrasi
│       │   │   └── style.css            : Styling umum aplikasi
│       │   ├── js/
│       │   │   └── app.js               : Script JavaScript umum aplikasi
│       │   └── main/
│       │       ├── css/
│       │       │   └── dashboard.css    : Styling khusus halaman dashboard
│       │       └── js/
│       │           └── dashboard.js     : Script JavaScript untuk halaman dashboard
│       │
│       └── templates/                   : Folder template HTML
│           ├── base.html                : Template dasar (layout utama yang diwarisi halaman lain)
│           ├── login.html               : Halaman login pengguna
│           ├── register.html            : Halaman registrasi anggota baru
│           ├── dashboard.html           : Halaman dashboard statistik sistem
│           ├── anggota/
│           │   ├── anggota_list.html    : Halaman daftar seluruh anggota perpustakaan
│           │   └── anggota_form.html    : Halaman form tambah/edit data anggota
│           ├── buku/
│           │   ├── buku_list.html       : Halaman daftar koleksi buku
│           │   ├── buku_detail.html     : Halaman detail informasi buku
│           │   └── buku_form.html       : Halaman form tambah/edit data buku
│           ├── peminjaman/
│           │   ├── peminjaman_list.html : Halaman daftar transaksi peminjaman
│           │   └── peminjaman_form.html : Halaman form pencatatan peminjaman
│           └── pengembalian/
│               ├── pengembalian_list.html  : Halaman daftar transaksi pengembalian
│               ├── pengembalian_form.html  : Halaman form pencatatan pengembalian
│               └── pengambalian_form.html  : Form alternatif pengembalian
│
└── requirements.txt                     : Daftar dependensi proyek (root)
```

---

### Cara Menjalankan

1. Pastikan **Python 3.x** dan **MySQL** sudah terinstal di sistem.

2. Clone repositori ini atau ekstrak file proyek.

3. Masuk ke direktori proyek dan install seluruh dependensi:

    ```bash
    cd perpustakaan
    pip install -r requirements.txt
    ```

4. Buat database MySQL dan sesuaikan konfigurasi pada file `perpustakaan/settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nama_database',
            'USER': 'username_mysql',
            'PASSWORD': 'password_mysql',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

5. Jalankan migrasi database:

    ```bash
    python manage.py migrate
    ```

6. Buat akun superuser (admin):

    ```bash
    python manage.py createsuperuser
    ```

7. Jalankan server pengembangan:

    ```bash
    python manage.py runserver
    ```

8. Akses aplikasi melalui browser pada alamat:

    ```
    http://127.0.0.1:8000/
    ```

---

### Teknologi yang Digunakan

| Komponen | Teknologi |
|---|---|
| Backend Framework | Django 5.0.1 |
| Database | MySQL (via PyMySQL 1.2.0) |
| Frontend | HTML, CSS, JavaScript |
| Python | 3.x |
| Autentikasi | Django Built-in Auth + Hashing |

---

### Fitur Utama

- **Login & Registrasi** — Anggota dapat mendaftar mandiri; data otomatis masuk ke halaman Anggota.
- **Dashboard** — Menampilkan statistik sistem secara ringkas untuk admin.
- **Manajemen Buku** — Admin dapat menambah, mengedit, dan menghapus data koleksi buku.
- **Peminjaman** — Anggota dapat meminjam buku langsung dari halaman buku dengan memilih tanggal kembali maksimal 7 hari; stok otomatis berkurang.
- **Pengembalian** — Admin mencatat pengembalian melalui tombol Kembalikan; status peminjaman berubah dan stok buku bertambah kembali.
- **Kontrol Akses Role** — Admin memiliki akses penuh; anggota hanya dapat melihat buku, peminjaman, dan pengembalian miliknya.
- **Sistem Sanksi** — Anggota yang terlambat mengembalikan buku akan dikenai sanksi berupa pemblokiran peminjaman selama jumlah hari terlambat dikalikan jumlah buku yang terlambat.
