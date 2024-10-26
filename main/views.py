from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Profile, Instruction
from .forms import CustomUserCreationForm, UserEditForm, ProfileEditForm, AddRecipeForm
import datetime

def show_main(request):
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
        'users': User.objects.all(),
        'last_login': request.COOKIES.get('last_login', 'Guest User'),
    }
    return render(request, "admin_dashboard.html", context)

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

def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            ingredients_list = form.cleaned_data['ingredients_list'].split(',')
            for ingredient_name in ingredients_list:
                ingredient_name = ingredient_name.strip()
                if ingredient_name:
                    ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
                    recipe.ingredients.add(ingredient)
            instructions_list = request.POST.getlist('instructions_list')
            for step_number, description in enumerate(instructions_list, start=1):
                description = description.strip()
                if description:
                    Instruction.objects.create(recipe=recipe, step_number=step_number, description=description)
            messages.success(request, "Recipe added successfully!")
            return redirect('main:show_main')
        else:
            messages.error(request, "Failed to add recipe. Please try again.")
            print(form.errors)
    else:
        form = AddRecipeForm()
    return render(request, 'add_recipe.html', {'form': form})

def search_recipes(request):
    queries = request.GET.dict()
    query = queries.get('query', '').strip()
    filter_type = queries.get('filter', 'none')
    recipes = Recipe.objects.all()
    if query:
        if filter_type == 'name':
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
    context = {'query': query, 'recipes': recipes}
    return render(request, 'search_results.html', context)

def get_user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_details.html', {'user': user})

@login_required(login_url='/login')
def edit_profile(request):
    user_form = UserEditForm(request.POST or None, instance=request.user)
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user.profile)

    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        
        profile = profile_form.save(commit=False)
        if 'hapus_foto' in request.POST:
            profile.profile_image = None  # Hapus foto profil
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('main:user_dashboard')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, "edit_profile.html", context)


@login_required(login_url='/login')
def redirect_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('main:show_admin')
    else:
        return redirect('main:user_dashboard')

@login_required(login_url='/login')
def user_dashboard(request):
    context = {
        'user': request.user,
        'last_login': request.COOKIES.get('last_login', 'Guest User'),
    }
    return render(request, 'user_dashboard.html', context)
