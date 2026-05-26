from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Buku, Anggota, Peminjaman, Pengembalian
from .forms import BukuForm, AnggotaForm, PeminjamanForm, PengembalianForm


def home(request):
    return redirect('dashboard')


@login_required
def dashboard(request):
    context = {
        'total_buku': Buku.objects.count(),
        'total_anggota': Anggota.objects.count(),
        'total_peminjaman': Peminjaman.objects.count(),
        'total_dipinjam': Peminjaman.objects.filter(status='dipinjam').count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def buku_list(request):
    buku = Buku.objects.all()
    return render(request, 'buku/buku_list.html', {'buku': buku})


@login_required
def buku_tambah(request):
    form = BukuForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('buku_list')
    return render(request, 'buku/buku_form.html', {'form': form})


@login_required
def buku_edit(request, id):
    buku = get_object_or_404(Buku, id=id)
    form = BukuForm(request.POST or None, instance=buku)
    if form.is_valid():
        form.save()
        return redirect('buku_list')
    return render(request, 'buku/buku_form.html', {'form': form})


@login_required
def buku_hapus(request, id):
    buku = get_object_or_404(Buku, id=id)
    buku.delete()
    return redirect('buku_list')


@login_required
def anggota_list(request):
    anggota = Anggota.objects.all()
    return render(request, 'anggota/anggota_list.html', {'anggota': anggota})


@login_required
def anggota_tambah(request):
    form = AnggotaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('anggota_list')
    return render(request, 'anggota/anggota_form.html', {'form': form})


@login_required
def peminjaman_list(request):
    peminjaman = Peminjaman.objects.all()
    return render(request, 'peminjaman/peminjaman_list.html', {'peminjaman': peminjaman})


@login_required
def peminjaman_tambah(request):
    form = PeminjamanForm(request.POST or None)
    if form.is_valid():
        peminjaman = form.save()
        buku = peminjaman.buku
        if buku.stok > 0:
            buku.stok -= 1
            buku.save()
        return redirect('peminjaman_list')
    return render(request, 'peminjaman/peminjaman_form.html', {'form': form})


@login_required
def pengembalian_list(request):
    pengembalian = Pengembalian.objects.all()
    return render(request, 'pengembalian/pengembalian_list.html', {'pengembalian': pengembalian})


@login_required
def pengembalian_tambah(request):
    form = PengembalianForm(request.POST or None)
    if form.is_valid():
        pengembalian = form.save()
        peminjaman = pengembalian.peminjaman
        peminjaman.status = 'dikembalikan'
        peminjaman.save()

        buku = peminjaman.buku
        buku.stok += 1
        buku.save()

        return redirect('pengembalian_list')
    return render(request, 'pengembalian/pengembalian_form.html', {'form': form})