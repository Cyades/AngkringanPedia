from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import Recipe, Ingredient
from .forms import AddRecipeForm, CustomUserEditForm

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
    form = CustomUserEditForm(instance=request.user)
    context = {
        'form' : form,
        'name': 'AngkringanPedia',
        'users' : User.objects.all(),
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "admin_dashboard.html", context)

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
    if not query:
        recipes = Recipe.objects.all()
        context = {
            'query': '',
            'recipes': recipes,
        }
        return render(request, 'search_results.html', context)
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
    context = {
        'query': query,
        'recipes': recipes,
    }
    return render(request, 'search_results.html', context)

@csrf_exempt    
def delete_product(request, id):
    if not request.user.is_superuser: 
        return HttpResponse(b"Forbidden", status=403)
    Recipe.objects.get(pk=id).delete()
    return HttpResponse(b"Success", status=204)
