from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import datetime
from .forms import CustomUserCreationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.urls import reverse, reverse_lazy

@login_required(login_url=reverse_lazy('authentication:login'))
def show_admin(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('dashboard:user_dashboard')
    
    users = User.objects.exclude(id=request.user.id)
    context = {
        'name': 'AngkringanPedia',
        'users': users,
        'last_login': request.COOKIES.get('last_login', 'Guest User'),
    }
    return render(request, "dashboard/admin_dashboard.html", context)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            is_admin = request.POST.get('is_admin') == 'on'
            user.is_staff = is_admin
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
            response = HttpResponseRedirect(reverse("main:show_admin" if user.is_staff or user.is_superuser else "main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    return HttpResponseRedirect(reverse('main:show_admin'))

@login_required(login_url='/login')
def edit_admin(request, id):
    admin = get_object_or_404(User, pk=id)
    form = UserEditForm(request.POST or None, request.FILES or None, instance=admin)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('main:show_admin'))
    context = {'form': form}
    return render(request, "edit_admin.html", context)

def get_user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_details.html', {'user': user})

@login_required(login_url=reverse_lazy('authentication:login'))
def edit_profile(request):
    user_form = UserEditForm(request.POST or None, instance=request.user)
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user.profile)

    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile = profile_form.save(commit=False)
        
        # Hapus foto jika diaktifkan
        if 'hapus_foto' in request.POST:
            profile.profile_image = None
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard:user_dashboard')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, "dashboard/edit_profile.html", context)


@login_required(login_url=reverse_lazy('authentication:login'))
def redirect_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('dashboard:show_admin')
    return redirect('dashboard:user_dashboard')


@login_required(login_url=reverse_lazy('authentication:login'))
def user_dashboard(request):
    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login', 'Guest User'),
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required(login_url=reverse_lazy('authentication:login'))
def edit_user(request, id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('dashboard:user_dashboard')
    
    user_to_edit = get_object_or_404(User, pk=id)
    user_form = UserEditForm(request.POST or None, instance=user_to_edit)
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=user_to_edit.profile)

    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile = profile_form.save(commit=False)
        if 'hapus_foto' in request.POST:
            profile.profile_image = None
        profile.save()

        messages.success(request, f'User {user_to_edit.username} updated successfully!')
        return redirect('dashboard:show_admin')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_to_edit': user_to_edit,
    }
    return render(request, "dashboard/edit_user.html", context)


@login_required(login_url=reverse_lazy('authentication:login'))
def delete_user(request, id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('dashboard:user_dashboard')
    
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect('dashboard:show_admin')
