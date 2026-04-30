from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # untuk akses admin
    path('', include('main.urls')),    # arahkan ke app kamu
]