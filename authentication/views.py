import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from authentication.models import Profile
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
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "id": user.id,
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "is_admin": user.is_staff or user.is_superuser,
            
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
        
# @csrf_exempt
# def register_flutter(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
        
#         print(f"Received data: {data}")  # Debug log untuk melihat input
        
#         username = data.get('username')
#         password1 = data.get('password1')
#         password2 = data.get('password2')
#         email = data.get('email')
#         phone_number = data.get('phone_number')
#         gender = data.get('gender')
#         profile_image = data.get('profile_image')  # Handle file upload

#         # Validasi password
#         if password1 != password2:
#             return JsonResponse({"status": False, "message": "Passwords do not match."}, status=400)

#         # Cek apakah username sudah ada
#         if User.objects.filter(username=username).exists():
#             return JsonResponse({"status": False, "message": "Username already exists."}, status=400)

#         # Simpan user menggunakan form
#         form_data = {
#             'username': username,
#             'email': email,
#             'password1': password1,
#             'password2': password2,
#         }

#         form = CustomUserCreationForm(form_data)
#         if form.is_valid():
#             user = form.save()
#             # Simpan profile tambahan (phone, gender, image)
#             profile = user.profile
#             profile.phone_number = phone_number
#             profile.gender = gender
#             if profile_image:
#                 # Convert profile image if needed
#                 profile.profile_image = profile_image  # Convert to InMemoryUploadedFile if necessary
#             profile.save()
#             return JsonResponse({"status": "success", "message": "User created successfully!"}, status=200)

#         return JsonResponse({"status": False, "message": "Form validation failed.", "errors": form.errors}, status=400)

#     return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

# @csrf_exempt
# def register_flutter(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(f"Received data: {data}")  # Debug log untuk melihat input

#             # Ambil data dari request
#             username = data.get('username')
#             password1 = data.get('password1')
#             password2 = data.get('password2')
#             email = data.get('email')
#             phone_number = data.get('phone_number')
#             gender = data.get('gender')
#             profile_image = data.get('profile_image')  # Handle file upload
#             is_admin = data.get('is_admin', False)

#             # Validasi password
#             if password1 != password2:
#                 return JsonResponse({"status": False, "message": "Passwords do not match."}, status=400)

#             # Cek apakah username sudah ada
#             if User.objects.filter(username=username).exists():
#                 return JsonResponse({"status": False, "message": "Username already exists."}, status=400)

#             # Konversi profile_image jika berbentuk base64
#             if profile_image:
#                 from django.core.files.base import ContentFile
#                 import base64
#                 format, imgstr = profile_image.split(';base64,')
#                 ext = format.split('/')[-1]
#                 profile_image = ContentFile(base64.b64decode(imgstr), name=f"{username}.{ext}")

#             # Simpan user menggunakan form
#             form_data = {
#                 'username': username,
#                 'email': email,
#                 'password1': password1,
#                 'password2': password2,
#                 'phone_number': phone_number,
#                 'gender': gender,
#                 'profile_image': profile_image,
#             }

#             form = CustomUserCreationForm(form_data)
#             if form.is_valid():
#                 user = form.save()

#                 # Atur status admin jika diperlukan
#                 if is_admin:
#                     user.is_staff = True
#                     user.save()

#                 return JsonResponse({"status": "success", "message": "User created successfully!"}, status=200)
#             else:
#                 print("Form Errors:", form.errors)  # Debug untuk mengetahui error detail

#             return JsonResponse({"status": False, "message": "Form validation failed.", "errors": form.errors}, status=400)

#         except Exception as e:
#             print(f"Error: {str(e)}")  # Log error
#             return JsonResponse({"status": False, "message": "An error occurred.", "error": str(e)}, status=500)

#     return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        try:
            # Ambil data dari request.POST
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            gender = request.POST.get('gender')
            is_admin = request.POST.get('is_admin', False) == 'true'  # Konversi ke boolean

            # Ambil file dari request.FILES
            profile_image = request.FILES.get('profile_image')

            # Validasi password
            if password1 != password2:
                return JsonResponse({"status": False, "message": "Passwords do not match."}, status=400)

            # Cek apakah username sudah ada
            if User.objects.filter(username=username).exists():
                return JsonResponse({"status": False, "message": "Username already exists."}, status=400)

            # Siapkan form data untuk CustomUserCreationForm
            form_data = {
                'username': username,
                'email': email,
                'password1': password1,
                'password2': password2,
                'phone_number': phone_number,
                'gender': gender,
                'profile_image': profile_image,  # Ini akan otomatis di-handle oleh Django
            }

            # Gunakan CustomUserCreationForm untuk menyimpan user
            form = CustomUserCreationForm(form_data, files=request.FILES)
            if form.is_valid():
                user = form.save()

                # Atur status admin
                if is_admin:
                    user.is_staff = True
                    user.save()

                return JsonResponse({"status": "success", "message": "User created successfully!"}, status=200)
            else:
                # print("Form Errors:", form.errors)  # Debug untuk mengetahui error detail
                return JsonResponse({"status": False, "message": "Form validation failed.", "errors": form.errors}, status=400)

        except Exception as e:
            # print(f"Error: {str(e)}")  # Log error
            return JsonResponse({"status": False, "message": "An error occurred.", "error": str(e)}, status=500)

    return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def logout_flutter(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
        
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
    
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_flutter(request, id):
    user = get_object_or_404(User, pk=id)

    if request.user == user:
        logout(request)
        user.delete()
        return JsonResponse({'message': 'Admin berhasil dihapus.', 'refresh': True}, status=200)
    else:
        user.delete()
        return JsonResponse({'message': 'Pengguna berhasil dihapus.', 'refresh': True}, status=200)

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

@csrf_exempt
def edit_user_flutter(request, id):
    try:
        user = get_object_or_404(User, pk=id)  # Ambil user berdasarkan ID

        if request.method == "POST":
            # Ambil data dari request.POST
            username = request.POST.get('username', user.username)  # Default ke username user
            email = request.POST.get('email', user.email)          # Default ke email user
            phone_number = request.POST.get('phone_number', user.profile.phone_number)
            # gender = request.POST.get('gender', user.profile.gender)
            profile_image = request.FILES.get('profile_image')  # Ambil file jika ada
            delete_profile_image = request.POST.get('delete_profile_image', 'false').lower() == 'true'

            # Perbarui User fields
            user.username = username
            user.email = email
            user.save()

            # Perbarui Profile fields
            user.profile.phone_number = phone_number
            # user.profile.gender = gender

            if delete_profile_image:
                # Jika user memilih untuk menghapus gambar profil
                user.profile.profile_image = "/profile_images/user.png"
                
            elif profile_image:
                user.profile.profile_image = profile_image  # Update profile image jika diberikan
                
            # if not profile_image:
            #     user.profile.profile_image = "/profile_images/user.png"

            user.profile.save()  # Simpan perubahan Profile

            # Return JSON success response
            return JsonResponse({"status": "success", "message": "Profile updated successfully!"}, status=200)

        return JsonResponse({"status": False, "message": "Invalid request method."}, status=400)

    except Exception as e:
        # print(f"Error: {str(e)}")  # Log error untuk debug
        return JsonResponse({"status": False, "message": "An error occurred.", "error": str(e)}, status=500)
    
# @csrf_exempt
# def edit_user_flutter(request, id):
#     user = get_object_or_404(User, pk=id)  # Ambil user berdasarkan ID
#     form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=user)  # Inisialisasi form

#     # Jika form valid, simpan perubahan
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({'success': True})
#         return HttpResponseRedirect(reverse('authentication:show_admin'))

#     # Kirim form dan user ke template
#     context = {
#         'form': form,
#         'user_to_edit': user,
#     }
#     return render(request, "edit_user.html", context)

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

def show_xml(request):
    data = Profile.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Profile.objects.select_related('user').all()  # Optimized query to include related user data
    profiles = []

    for profile in data:
        profiles.append({
            "model": "authentication.profile",
            "pk": profile.pk,
            "fields": {
                "user": profile.user.id,
                "username": profile.user.username,
                "email": profile.user.email,
                "phone_number": profile.phone_number,
                "gender": profile.gender,
                "is_admin": "Admin" if profile.user.is_staff else "User",
                "profile_image": profile.profile_image.url if profile.profile_image else "/media/profile_images/user.png",
            }
        })

    return JsonResponse(profiles, safe=False)

# @csrf_exempt
# def user_detail(request, id):
#     try:
#         # print(f"Request method: {request.method}, ID: {id}")
#         user = get_object_or_404(Profile, user_id=id)
#         data = {
#             "username": user.user.username,
#             "email": user.user.email,
#             "phone_number": user.phone_number,
#             "gender": user.gender,
#             "profile_image": user.profile_image.url if user.profile_image else None,
#         }
#         # print("Data sent:", data)
#         return JsonResponse(data, safe=False)
#     except Exception as e:
#         # print("Error in user_detail:", str(e))
#         return JsonResponse({"error": str(e)}, status=500)
### build

@csrf_exempt
def user_detail(request, id):
    try:
        # Mengambil data profil berdasarkan user_id
        user_profile = get_object_or_404(Profile.objects.select_related('user'), user_id=id)
        
        # Menyesuaikan format data seperti pada `show_json`
        data = {
            "model": "authentication.profile",
            "pk": user_profile.pk,
            "fields": {
                "user": user_profile.user.id,
                "username": user_profile.user.username,
                "email": user_profile.user.email,
                "phone_number": user_profile.phone_number,
                "gender": user_profile.gender,
                "is_admin": "Admin" if user_profile.user.is_staff else "User",
                "profile_image": user_profile.profile_image.url if user_profile.profile_image else "/media/profile_images/user.png",
            }
        }
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)