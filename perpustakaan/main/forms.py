from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Anggota, Buku, Peminjaman, Pengembalian


class RegisterForm(UserCreationForm):
    nama = forms.CharField(max_length=100, label='Nama')
    nim = forms.CharField(max_length=30, label='NIM')
    email = forms.EmailField(required=True, label='Email')
    no_hp = forms.CharField(max_length=20, label='No HP')
    alamat = forms.CharField(
        required=False,
        label='Alamat',
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields([
            'username',
            'nama',
            'nim',
            'email',
            'no_hp',
            'alamat',
            'password1',
            'password2',
        ])

    def clean_nim(self):
        nim = self.cleaned_data['nim']

        if Anggota.objects.filter(nim=nim).exists():
            raise forms.ValidationError('NIM sudah terdaftar.')

        return nim

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            Anggota.objects.update_or_create(
                user=user,
                defaults={
                    'nama': self.cleaned_data['nama'],
                    'nim': self.cleaned_data['nim'],
                    'email': self.cleaned_data['email'],
                    'no_hp': self.cleaned_data['no_hp'],
                    'alamat': self.cleaned_data['alamat'],
                }
            )

        return user


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
        widgets = {
            'tanggal_pinjam': forms.DateInput(attrs={'type': 'date'}),
            'tanggal_kembali': forms.DateInput(attrs={'type': 'date'}),
        }

class PengembalianForm(forms.ModelForm):
    class Meta:
        model = Pengembalian
        fields = '__all__'
        widgets = {
            'tanggal_dikembalikan': forms.DateInput(attrs={'type': 'date'}),
        }
