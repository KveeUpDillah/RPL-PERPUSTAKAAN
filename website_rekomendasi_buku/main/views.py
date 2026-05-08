from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    return render(request, 'favorites.html')


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

        # USER BARU MASUK DATABASE DJANGO
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