import json
import requests

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# ======================
# STORAGE FAVORITE
# ======================

favorite_books = []


# ======================
# TOGGLE FAVORITE
# ======================

@require_POST
@login_required(login_url='login')
def toggle_favorite(request):

    data = json.loads(request.body)

    key = data.get('key')

    existing = next(
        (b for b in favorite_books if b['key'] == key),
        None
    )

    # HAPUS FAVORITE
    if existing:

        favorite_books.remove(existing)

        return JsonResponse({
            'status': 'removed'
        })

    # TAMBAH FAVORITE
    favorite_books.append(data)

    return JsonResponse({
        'status': 'added'
    })


# ======================
# API POPULAR BOOKS
# ======================

def popular_books(request):

    url = "https://openlibrary.org/search.json?q=python&limit=6&page=1"

    response = requests.get(url)

    books = []

    if response.status_code == 200:

        data = response.json()

        for item in data.get('docs', [])[:6]:

            cover_id = item.get('cover_i')

            cover_url = None

            if cover_id:
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

            books.append({
                'key': item.get('key'),
                'title': item.get('title'),
                'author': item.get('author_name', ['Unknown'])[0],
                'year': item.get('first_publish_year'),
                'cover_url': cover_url,
                'language': 'English',
                'description': 'Book from OpenLibrary API',
                'is_favorite': any(
                    b['key'] == item.get('key')
                    for b in favorite_books
                )
            })

    return JsonResponse({
        'books': books
    })


# ======================
# API SEARCH BOOKS
# ======================

def search_books(request):

    query = request.GET.get('q', '').strip()

    page = request.GET.get('page', 1)

    if not query:
        return JsonResponse({
            'books': [],
            'total': 0
        })

    limit = 20

    # SEARCH HANYA BERDASARKAN JUDUL
    url = (
        f"https://openlibrary.org/search.json"
        f"?title={query}&page={page}&limit={limit}"
    )

    response = requests.get(url)

    books = []

    total = 0

    if response.status_code == 200:

        data = response.json()

        total = data.get('numFound', 0)

        for item in data.get('docs', []):

            cover_id = item.get('cover_i')

            cover_url = None

            if cover_id:
                cover_url = (
                    f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                )

            books.append({
                'key': item.get('key'),
                'title': item.get('title'),
                'author': item.get('author_name', ['Unknown'])[0],
                'year': item.get('first_publish_year'),
                'cover_url': cover_url,
                'language': 'English',
                'description': 'Book from OpenLibrary API',
                'is_favorite': any(
                    b['key'] == item.get('key')
                    for b in favorite_books
                )
            })

    return JsonResponse({
        'books': books,
        'total': total
    })


# ======================
# HOME
# ======================

@login_required(login_url='login')
def home(request):

    return render(request, 'home.html')


# ======================
# AI SEARCH
# ======================

@login_required(login_url='login')
def ai_search(request):

    return render(request, 'ai-search.html')


# ======================
# FAVORITES
# ======================

@login_required(login_url='login')
def favorites(request):

    return render(request, 'favorites.html', {
        'favorites': favorite_books
    })


# ======================
# CONTACT
# ======================

@login_required(login_url='login')
def contact(request):

    return render(request, 'contact.html')


# ======================
# LOGIN
# ======================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

    return render(request, 'auth/login.html')


# ======================
# REGISTER
# ======================

def register_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'auth/register.html')


# ======================
# LOGOUT
# ======================

def logout_view(request):

    logout(request)

    return redirect('login')