# website-Perpustakaan
# Sistem Informasi Perpustakaan Berbasis Web


Sudah ditambahkan pembagian akses antara admin dan user: user hanya bisa melihat buku, peminjaman, dan pengembalian, sedangkan admin tetap bisa mengelola data. Saat user registrasi, datanya otomatis masuk ke halaman Anggota dan bisa diedit oleh admin. User juga bisa meminjam buku langsung dari halaman Buku dengan memilih tanggal pengembalian maksimal 7 hari, lalu data otomatis masuk ke halaman Peminjaman dan stok buku berkurang.

Untuk admin, tombol tambah manual pada Peminjaman, Pengembalian, dan Anggota sudah dihapus agar alurnya lebih rapi. Admin bisa mencatat buku yang sudah dikembalikan dari halaman Peminjaman melalui tombol Kembalikan; setelah itu data otomatis masuk ke halaman Pengembalian, status peminjaman berubah, dan stok buku bertambah lagi. Ditambahkan juga sistem sanksi keterlambatan: jika user telat mengembalikan buku, akun user tidak bisa meminjam selama jumlah hari telat dikalikan jumlah buku yang telat, dan tanggal sanksinya terlihat di halaman Anggota.