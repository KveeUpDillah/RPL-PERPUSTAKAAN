from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST
from .models import Buku, Anggota, Peminjaman, Pengembalian, Aktivitas, default_nim_for_user
from .forms import RegisterForm, BukuForm, AnggotaForm, PeminjamanForm, PengembalianForm
from .decorators import admin_required

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })

def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')

    return redirect('buku_list')

@admin_required
def dashboard(request):
    aktivitas_terbaru = Aktivitas.objects.all().order_by('-waktu')[:5]

    context = {
        'total_buku': Buku.objects.count(),
        'total_anggota': Anggota.objects.count(),
        'total_peminjaman': Peminjaman.objects.count(),
        'total_dipinjam': Peminjaman.objects.filter(status='dipinjam').count(),
        'aktivitas_terbaru': aktivitas_terbaru,
    }
    return render(request, 'dashboard.html', context)


@login_required
def buku_list(request):
    buku = Buku.objects.all()
    today = timezone.localdate()

    return render(request, 'buku/buku_list.html', {
    'buku': buku,
    'today': today,
    'max_return_date': today + timedelta(days=7),
    })


@login_required
@require_POST
def buku_pinjam(request, id):
    if request.user.is_staff:
        messages.warning(request, 'Admin dapat mencatat peminjaman melalui menu Peminjaman.')
        return redirect('buku_list')

    anggota, created = Anggota.objects.get_or_create(
        user=request.user,
        defaults={
            'nama': request.user.get_full_name() or request.user.username,
            'nim': default_nim_for_user(request.user),
            'email': request.user.email or '',
            'no_hp': '-',
            'alamat': '',
        }
    )

    tanggal_pinjam = timezone.localdate()

    tanggal_kembali = parse_date(request.POST.get('tanggal_kembali', ''))
    max_tanggal_kembali = tanggal_pinjam + timedelta(days=7)

    if not tanggal_kembali:
        messages.error(request, 'Pilih tanggal pengembalian terlebih dahulu.')
        return redirect('buku_list')
    
    #if tanggal_kembali < tanggal_pinjam:
       # messages.error(request, 'Tanggal pengembalian tidak boleh sebelum tanggal pinjam.')
        #return redirect('buku_list')

    if tanggal_kembali > max_tanggal_kembali:
        messages.error(request, 'Tanggal pengembalian maksimal 7 hari dari tanggal pinjam.')
        return redirect('buku_list')

    with transaction.atomic():
        buku = get_object_or_404(Buku.objects.select_for_update(), id=id)

        if buku.stok <= 0:
            messages.error(request, f"Stok buku {buku.judul} sedang habis.")
            return redirect('buku_list')

        sudah_dipinjam = Peminjaman.objects.filter(
            anggota=anggota,
            buku=buku,
            status='dipinjam',
        ).exists()

        if sudah_dipinjam:
            messages.warning(request, f"Kamu masih meminjam buku {buku.judul}.")
            return redirect('peminjaman_list')

        Peminjaman.objects.create(
            anggota=anggota,
            buku=buku,
            tanggal_pinjam=tanggal_pinjam,
            tanggal_kembali=tanggal_kembali,
            status='dipinjam',
        )

        buku.stok -= 1
        buku.save(update_fields=['stok'])

        Aktivitas.objects.create(
            user=request.user,
            aksi='Tambah',
            model='Peminjaman',
            keterangan=f"Meminjam buku: {buku.judul}"
        )

    messages.success(request, f"Buku {buku.judul} berhasil dipinjam.")
    return redirect('peminjaman_list')


@admin_required
def buku_tambah(request):
    form = BukuForm(request.POST or None)

    if form.is_valid():
        buku = form.save()

        Aktivitas.objects.create(
            user=request.user,
            aksi='Tambah',
            model='Buku',
            keterangan=f"Menambahkan buku: {buku.judul}"
        )

        return redirect('buku_list')

    return render(request, 'buku/buku_form.html', {'form': form})

@admin_required
def buku_edit(request, id):
    buku = get_object_or_404(Buku, id=id)
    form = BukuForm(request.POST or None, instance=buku)

    if form.is_valid():
        buku = form.save()

        Aktivitas.objects.create(
            user=request.user,
            aksi='Edit',
            model='Buku',
            keterangan=f"Mengedit buku: {buku.judul}"
        )

        return redirect('buku_list')

    return render(request, 'buku/buku_form.html', {'form': form})


@admin_required
def buku_hapus(request, id):
    buku = get_object_or_404(Buku, id=id)
    judul_buku = buku.judul

    buku.delete()

    Aktivitas.objects.create(
        user=request.user,
        aksi='Hapus',
        model='Buku',
        keterangan=f"Menghapus buku: {judul_buku}"
    )

    return redirect('buku_list')


@admin_required
def anggota_list(request):
    anggota = Anggota.objects.all()
    return render(request, 'anggota/anggota_list.html', {'anggota': anggota})


@admin_required
def anggota_tambah(request):
    form = AnggotaForm(request.POST or None)

    if form.is_valid():
        anggota = form.save()

        Aktivitas.objects.create(
            user=request.user,
            aksi='Tambah',
            model='Anggota',
            keterangan=f"Menambahkan anggota: {anggota.nama}"
        )

        return redirect('anggota_list')

    return render(request, 'anggota/anggota_form.html', {'form': form})


@admin_required
def anggota_edit(request, id):
    anggota = get_object_or_404(Anggota, id=id)
    form = AnggotaForm(request.POST or None, instance=anggota)

    if form.is_valid():
        anggota = form.save()

        Aktivitas.objects.create(
            user=request.user,
            aksi='Edit',
            model='Anggota',
            keterangan=f"Mengedit anggota: {anggota.nama}"
        )

        return redirect('anggota_list')

    return render(request, 'anggota/anggota_form.html', {'form': form})


@admin_required
def hapus_anggota(request, id):
    anggota = get_object_or_404(Anggota, id=id)

    nama_anggota = anggota.nama

    if anggota.user:
        anggota.user.delete()
    else:
        anggota.delete()

    Aktivitas.objects.create(
        user=request.user,
        aksi='Hapus',
        model='Anggota',
        keterangan=f"Menghapus anggota: {nama_anggota}"
    )

    return redirect('anggota_list')

@login_required
def peminjaman_list(request):
    peminjaman = Peminjaman.objects.select_related('anggota', 'buku').all()

    if not request.user.is_staff:
        peminjaman = peminjaman.filter(anggota__user=request.user)

    return render(request, 'peminjaman/peminjaman_list.html', {'peminjaman': peminjaman})


@admin_required
def peminjaman_tambah(request):
    form = PeminjamanForm(request.POST or None)

    if form.is_valid():
        peminjaman = form.save()
        buku = peminjaman.buku

        if buku.stok > 0:
            buku.stok -= 1
            buku.save()

        Aktivitas.objects.create(
            user=request.user,
            aksi='Tambah',
            model='Peminjaman',
            keterangan=f"Menambahkan peminjaman buku: {buku.judul}"
        )

        return redirect('peminjaman_list')

    return render(request, 'peminjaman/peminjaman_form.html', {'form': form})


@admin_required
@require_POST
def peminjaman_kembalikan(request, id):
    with transaction.atomic():
        peminjaman = get_object_or_404(
            Peminjaman.objects.select_for_update().select_related('anggota', 'buku'),
            id=id,
        )

        if peminjaman.status == 'dikembalikan' or hasattr(peminjaman, 'pengembalian'):
            messages.warning(request, 'Peminjaman ini sudah tercatat sebagai pengembalian.')
            return redirect('pengembalian_list')

        peminjaman.status = 'dikembalikan'
        peminjaman.save(update_fields=['status'])

        buku = peminjaman.buku
        buku.stok += 1
        buku.save(update_fields=['stok'])

        hari_telat = max(
            (timezone.localdate() - peminjaman.tanggal_kembali).days,
            0
        )

        denda = hari_telat * 1000  # Rp1000 per hari

        pengembalian = Pengembalian.objects.create(
            peminjaman=peminjaman,
            tanggal_dikembalikan=timezone.localdate(),
            denda=denda,
        )

        Aktivitas.objects.create(
            user=request.user,
            aksi='Tambah',
            model='Pengembalian',
            keterangan=f"Mencatat pengembalian buku: {buku.judul}"
        )

    if hari_telat > 0:
        messages.warning(
            request,
            f"Buku {pengembalian.peminjaman.buku.judul} dikembalikan terlambat {hari_telat} hari. "
            f"Denda yang harus dibayar sebesar Rp{denda:,}."
        )
    else:
        messages.success(
            request,
            f"Buku {pengembalian.peminjaman.buku.judul} berhasil dicatat sebagai pengembalian."
        )

    return redirect('pengembalian_list')


@login_required
def pengembalian_list(request):
    pengembalian = Pengembalian.objects.select_related('peminjaman__anggota', 'peminjaman__buku').all()

    if not request.user.is_staff:
        pengembalian = pengembalian.filter(peminjaman__anggota__user=request.user)

    return render(request, 'pengembalian/pengembalian_list.html', {'pengembalian': pengembalian})


@admin_required
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

        Aktivitas.objects.create(
            user=request.user,
            aksi='Tambah',
            model='Pengembalian',
            keterangan=f"Menambahkan pengembalian buku: {buku.judul}"
        )

        return redirect('pengembalian_list')

    return render(request, 'pengembalian/pengembalian_form.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('login')
