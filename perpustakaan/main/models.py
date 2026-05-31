from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Anggota(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    no_hp = models.CharField(max_length=20)
    alamat = models.TextField(blank=True)
    sanksi_sampai = models.DateField(null=True, blank=True)

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

class Aktivitas(models.Model):
    AKSI_CHOICES = [
        ('Tambah', 'Tambah'),
        ('Edit', 'Edit'),
        ('Hapus', 'Hapus'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    aksi = models.CharField(max_length=20, choices=AKSI_CHOICES)
    model = models.CharField(max_length=100)
    keterangan = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aksi} {self.model} - {self.waktu}"


def default_nim_for_user(user):
    base_nim = f"USER-{user.pk}"
    nim = base_nim[:30]
    counter = 1

    while Anggota.objects.filter(nim=nim).exists():
        suffix = f"-{counter}"
        nim = f"{base_nim[:30 - len(suffix)]}{suffix}"
        counter += 1

    return nim


@receiver(post_save, sender=User)
def create_anggota_for_new_user(sender, instance, created, **kwargs):
    if not created or instance.is_staff or instance.is_superuser:
        return

    Anggota.objects.get_or_create(
        user=instance,
        defaults={
            'nama': instance.get_full_name() or instance.username,
            'nim': default_nim_for_user(instance),
            'email': instance.email or '',
            'no_hp': '-',
            'alamat': '',
        }
    )
