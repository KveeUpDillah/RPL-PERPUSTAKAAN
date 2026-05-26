from django.contrib import admin
from .models import Anggota, Buku, Peminjaman, Pengembalian


@admin.register(Anggota)
class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'nim', 'email', 'no_hp')
    search_fields = ('nama', 'nim', 'email')


@admin.register(Buku)
class BukuAdmin(admin.ModelAdmin):
    list_display = ('id', 'judul', 'penulis', 'penerbit', 'tahun_terbit', 'kategori', 'stok')
    search_fields = ('judul', 'penulis', 'kategori')
    list_filter = ('kategori', 'tahun_terbit')


@admin.register(Peminjaman)
class PeminjamanAdmin(admin.ModelAdmin):
    list_display = ('id', 'anggota', 'buku', 'tanggal_pinjam', 'tanggal_kembali', 'status')
    search_fields = ('anggota__nama', 'buku__judul')
    list_filter = ('status',)


@admin.register(Pengembalian)
class PengembalianAdmin(admin.ModelAdmin):
    list_display = ('id', 'peminjaman', 'tanggal_dikembalikan', 'denda')