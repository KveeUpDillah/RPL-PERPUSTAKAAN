from django import forms
from .models import Anggota, Buku, Peminjaman, Pengembalian


class AnggotaForm(forms.ModelForm):
    class Meta:
        model = Anggota
        fields = '__all__'


class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = '__all__'


class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman
        fields = '__all__'


class PengembalianForm(forms.ModelForm):
    class Meta:
        model = Pengembalian
        fields = '__all__'