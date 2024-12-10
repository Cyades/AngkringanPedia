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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
import json
from .models import Recipe, Ingredient, Instruction
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Recipe

def show_main(request):
    # Jika pengguna tidak login, atur 'last_login' ke None atau pesan default
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
    if(not request.user.is_superuser and not request.user.is_staff): return
    Recipe.objects.get(pk=id).delete()
    return HttpResponse(b"Success", status=204)


# views.py in Django main app
from django.http import JsonResponse
from .models import Recipe, Ingredient, Instruction
from django.views.decorators.csrf import csrf_exempt
import json

def get_recipes(request):
    recipes = Recipe.objects.all()
    data = []
    for recipe in recipes:
        recipe_data = {
            'id': recipe.id,
            'recipe_name': recipe.recipe_name,
            'cooking_time': recipe.cooking_time,
            'servings': recipe.servings,
            'image_url': recipe.image_url,
            'ingredients': [{'name': ingredient.name} for ingredient in recipe.ingredients.all()],
            'instructions': recipe.instructions
        }
        data.append(recipe_data)
    return JsonResponse({'recipes': data})

@csrf_exempt
def search_recipes_api(request):
    query = request.GET.get('query', '').strip()
    filter_type = request.GET.get('filter', 'none')
    
    if not query:
        recipes = Recipe.objects.all()
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
    
    data = []
    for recipe in recipes:
        recipe_data = {
            'id': recipe.id,
            'recipe_name': recipe.recipe_name,
            'cooking_time': recipe.cooking_time,
            'servings': recipe.servings,
            'image_url': recipe.image_url,
            'ingredients': [{'name': ingredient.name} for ingredient in recipe.ingredients.all()],
            'instructions': recipe.instructions
        }
        data.append(recipe_data)
    return JsonResponse({'recipes': data})

# Add this new view to get CSRF token
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt  # For development only
@require_http_methods(["POST"])
def add_recipe_api(request):
    try:
        data = json.loads(request.body)
        
        # Create recipe
        recipe = Recipe.objects.create(
            recipe_name=data['recipe_name'],
            cooking_time=data['cooking_time'],
            servings=data['servings'],
            image_url=data['image_url'],
            instructions=''
        )
        
        # Add ingredients
        ingredients_list = data['ingredients_list'].split(',')
        for ingredient_name in ingredients_list:
            ingredient_name = ingredient_name.strip()
            if ingredient_name:
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
                recipe.ingredients.add(ingredient)

        # Add instructions
        instructions_list = data['instructions_list']
        instruction_text = []
        for step_number, description in enumerate(instructions_list, start=1):
            if description.strip():
                Instruction.objects.create(
                    recipe=recipe,
                    step_number=step_number,
                    description=description.strip()
                )
                instruction_text.append(f"{step_number}. {description.strip()}")

        # Update recipe with combined instructions
        recipe.instructions = "\n".join(instruction_text)
        recipe.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Recipe added successfully',
            'recipe_id': recipe.id
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except KeyError as e:
        return JsonResponse({
            'success': False,
            'message': f'Missing required field: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
    

@csrf_exempt
def delete_product(request, id):
    if request.method == 'DELETE':
        try:
            recipe = Recipe.objects.get(pk=id)
            recipe.delete()
            return HttpResponse(status=204)
        except Recipe.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)