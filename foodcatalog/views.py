from django.shortcuts import render
from main.models import Recipe  # Mengimpor model Recipe dari aplikasi lain

def search_recipe_by_name(request, recipe_name):  # Mengambil parameter dari URL
    # Filter resep berdasarkan nama yang cocok
    recipes = Recipe.objects.filter(recipe_name__icontains=recipe_name)

    context = {
        'recipe_name': recipe_name,
        'recipes': recipes,
    }
    return render(request, 'show_recipe.html', context)

def show_main(request):
    context = {
        'name': 'AngkringanPedia',
        'recipes': Recipe.objects.all()
    }
    return render(request, "main.html", context)