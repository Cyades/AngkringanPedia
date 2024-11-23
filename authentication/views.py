from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
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
from .forms import CustomUserEditForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods


# Create your views here.
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
            return redirect('authentication:login')
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
                response = HttpResponseRedirect(reverse("authentication:show_admin"))
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
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/authentication/login/')
@require_http_methods(["DELETE"])
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)

    if request.user == user:
        logout(request)
        user.delete()
        return JsonResponse({'message': 'Admin berhasil dihapus.', 'refresh': True}, status=200)
    else:
        user.delete()
        return JsonResponse({'message': 'Pengguna berhasil dihapus.', 'refresh': False}, status=200)

def edit_admin(request, id):
    admin = get_object_or_404(User, pk=id)
    form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=admin)

    # Cek jika request adalah POST dan form valid
    if request.method == "POST" and form.is_valid():
        form.save()
        
        # Cek apakah request ini AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})  # Kirim respon JSON jika permintaan adalah AJAX
        else:
            return HttpResponseRedirect(reverse('authentication:show_admin'))

    context = {'form': form}
    return render(request, "edit_admin.html", context)

def get_user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_details.html', {'user': user})

@login_required(login_url='/login')
def edit_user(request, id):
    user = get_object_or_404(User, pk=id)  # Ambil user berdasarkan ID
    form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=user)  # Inisialisasi form

    # Jika form valid, simpan perubahan
    if request.method == "POST" and form.is_valid():
        form.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return HttpResponseRedirect(reverse('authentication:show_admin'))

    # Kirim form dan user ke template
    context = {
        'form': form,
        'user_to_edit': user,
    }
    return render(request, "edit_user.html", context)

@login_required(login_url='/authentication/login/')
def show_admin(request):
    form = CustomUserEditForm(instance=request.user)
    context = {
        'form' : form,
        'name': 'AngkringanPedia',
        'users' : User.objects.all(),
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "admin_dashboard.html", context)
