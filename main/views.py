from django.shortcuts import render
from django.db.models import Q
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.models import *

def show_main(request):
    # Jika pengguna tidak login, atur 'last_login' ke None atau pesan default
    last_login = request.COOKIES.get('last_login', 'Guest User')

    context = {
        'name': 'AngkringanPedia',
        'recipes': Recipe.objects.all(),
        'last_login': last_login,
    }
    return render(request, "main.html", context)

@login_required(login_url='/login')
def show_admin(request):
    context = {
        'name': 'AngkringanPedia',
        'users' : User.objects.all(),
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "admin_dashboard.html", context)

def search_recipes(request):
    query = request.GET.get('query', '')  # Ambil query dari user
    # Ambil filter yang digunakan
    filter_type = request.GET.get('none_query') or request.GET.get('ingredient_query') or request.GET.get('name_query')

    if filter_type == 'none':
        recipes = Recipe.objects.filter(
            Q(recipe_name__icontains=query) |
            Q(ingredients__name__icontains=query) |
            Q(servings__icontains=query) |
            Q(cooking_time__icontains=query) |
            Q(recipe_instructions__description__icontains=query)
        ).distinct()
    elif filter_type == 'name':
        recipes = Recipe.objects.filter(recipe_name__icontains=query).distinct()
    elif filter_type == 'ingredient':
        recipes = Recipe.objects.filter(ingredients__name__icontains=query).distinct()
    else:
        recipes = Recipe.objects.filter(
            Q(recipe_name__icontains=query) | 
            Q(ingredients__name__icontains=query) |
            Q(servings__icontains=query) | 
            Q(cooking_time__icontains=query) | 
            Q(recipe_instructions__description__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'recipes': recipes,
    }
    return render(request, 'search_results.html', context)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Cek apakah pengguna terdaftar sebagai admin
            is_admin = request.POST.get('is_admin') == 'on'
            user.is_staff = is_admin  # Set is_staff menjadi True jika admin
            user.save()

            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Cek apakah user adalah admin
            if user.is_staff or user.is_superuser:
                response = HttpResponseRedirect(reverse("main:show_admin"))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
                # Ganti dengan URL halaman admin

            # Jika bukan admin, arahkan ke halaman utama
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    
    # Hapus pengguna
    user.delete()
    
    # Kembali ke halaman admin setelah menghapus pengguna
    return HttpResponseRedirect(reverse('main:show_admin'))