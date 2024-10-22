from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'AngkringanPedia'
    }
    return render(request, "main.html", context)

from django.shortcuts import render
from .models import Recipe

def recipe_list(request):
    # Ambil semua data resep dari model Recipe
    recipes = Recipe.objects.all()
    
    # Kirim data ke template
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})
