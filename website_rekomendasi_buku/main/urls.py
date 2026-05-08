from django.urls import path
from .views import *

urlpatterns = [

    path('', home, name='home'),

    path('ai-search/', ai_search, name='ai_search'),

    path('favorites/', favorites, name='favorites'),

    path('contact/', contact, name='contact'),

    path('login/', login_view, name='login'),

    path('register/', register_view, name='register'),

    path('logout/', logout_view, name='logout'),
]