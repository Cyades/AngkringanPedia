from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.models import *
from .models import Recipe, Ingredient
from .forms import AddRecipeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Profile, Instruction
from .forms import CustomUserCreationForm, UserEditForm, ProfileEditForm, AddRecipeForm, CustomUserEditForm
import datetime

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Guest User')
    context = {
        'name': 'AngkringanPedia',
        'recipes': Recipe.objects.all(),
        'last_login': last_login,
    }
    return render(request, "main.html", context)

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

@csrf_exempt    
def delete_product(request, id):
    if(not request.user.is_superuser and not request.user.is_staff): return
    Recipe.objects.get(pk=id).delete()
    return HttpResponse(b"Success", status=204)
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

@login_required(login_url='/login')
def edit_user(request, id):
    user_to_edit = get_object_or_404(User, pk=id)
    user_form = UserEditForm(request.POST or None, instance=user_to_edit)
    profile_form = ProfileEditForm(request.POST or None, request.FILES or None, instance=user_to_edit.profile)

    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile = profile_form.save(commit=False)
        if 'hapus_foto' in request.POST:
            profile.profile_image = None  # Remove profile picture if the option is selected
        profile.save()
        
        messages.success(request, f'User {user_to_edit.username} updated successfully!')
        return redirect('main:show_admin')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_to_edit': user_to_edit,
    }
    return render(request, "edit_user.html", context)
