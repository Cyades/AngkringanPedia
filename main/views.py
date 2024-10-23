from django.shortcuts import render
from django.db.models import Q
from .models import Recipe

def show_main(request):
    context = {
        'name': 'AngkringanPedia',
        'recipes': Recipe.objects.all()
    }
    return render(request, "main.html", context)

def search_recipes(request):
    query = request.GET.get('query', '')  # Ambil query dari user
    # Ambil filter yang digunakan
    filter_type = request.GET.get('none_query') or request.GET.get('ingredient_query') or request.GET.get('name_query')

    if filter_type == 'none':
        print("0")
        recipes = Recipe.objects.filter(
            Q(recipe_name__icontains=query) |
            Q(ingredients__name__icontains=query) |
            Q(servings__icontains=query) |
            Q(cooking_time__icontains=query) |
            Q(recipe_instructions__description__icontains=query)
        ).distinct()
    elif filter_type == 'name':
        print("1")
        recipes = Recipe.objects.filter(recipe_name__icontains=query).distinct()
    elif filter_type == 'ingredient':
        print("2")
        recipes = Recipe.objects.filter(ingredients__name__icontains=query).distinct()
    else:
        print("3")
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

