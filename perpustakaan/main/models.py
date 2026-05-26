from django.db import models
from django.contrib.auth.models import User


class Anggota(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    no_hp = models.CharField(max_length=20)
    alamat = models.TextField(blank=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Anggota"
        verbose_name_plural = "Anggota"


class Buku(models.Model):
    judul = models.CharField(max_length=150)
    penulis = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=100)
    tahun_terbit = models.IntegerField()
    kategori = models.CharField(max_length=100)
    stok = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name = "Buku"
        verbose_name_plural = "Buku"


class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('dipinjam', 'Dipinjam'),
        ('dikembalikan', 'Dikembalikan'),
        ('terlambat', 'Terlambat'),
    ]

    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dipinjam')

    def __str__(self):
        return f"{self.anggota.nama} - {self.buku.judul}"

    class Meta:
        verbose_name = "Peminjaman"
        verbose_name_plural = "Peminjaman"


class Pengembalian(models.Model):
    peminjaman = models.OneToOneField(Peminjaman, on_delete=models.CASCADE)
    tanggal_dikembalikan = models.DateField()
    denda = models.IntegerField(default=0)

    def __str__(self):
        return f"Pengembalian {self.peminjaman.buku.judul}"

    class Meta:
        verbose_name = "Pengembalian"
        verbose_name_plural = "Pengembalian"