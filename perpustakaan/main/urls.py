from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('buku/', views.buku_list, name='buku_list'),
    path('buku/tambah/', views.buku_tambah, name='buku_tambah'),
    path('buku/edit/<int:id>/', views.buku_edit, name='buku_edit'),
    path('buku/hapus/<int:id>/', views.buku_hapus, name='buku_hapus'),

    path('anggota/', views.anggota_list, name='anggota_list'),
    path('anggota/tambah/', views.anggota_tambah, name='anggota_tambah'),

    path('peminjaman/', views.peminjaman_list, name='peminjaman_list'),
    path('peminjaman/tambah/', views.peminjaman_tambah, name='peminjaman_tambah'),

    path('pengembalian/', views.pengembalian_list, name='pengembalian_list'),
    path('pengembalian/tambah/', views.pengembalian_tambah, name='pengembalian_tambah'),
]