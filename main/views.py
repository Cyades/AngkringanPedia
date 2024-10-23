from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Recipe
from .forms import AddRecipeForm
from django.http import HttpResponseRedirect
from django.urls import reverse



def show_main(request):
    context = {
        'name': 'AngkringanPedia',
        'recipes': Recipe.objects.all()
    }
    return render(request, "main.html", context)

def search_recipes(request):
    queries = request.GET.dict()

    if not queries:
        return render(request, 'search_results.html')

    query = queries['none_query'] if queries.get('none_query') else (
        queries['name_query'] if queries.get('name_query') else(
            queries.get('ingredient_query')
        )
    )

    if queries.get('none_query'):
        recipes = Recipe.objects.filter(
            Q(recipe_name__icontains=query) |
            Q(ingredients__name__icontains=query) |
            Q(servings__icontains=query) |
            Q(cooking_time__icontains=query) |
            Q(recipe_instructions__description__icontains=query)
        ).distinct()
    elif queries.get('name_query'):
        recipes = Recipe.objects.filter(recipe_name__icontains=query).distinct()
    elif queries.get('ingredient_query'):
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

def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:show_main'))
    else:
        form = AddRecipeForm()

    return render(request, 'add_recipe.html', {'form': form})
