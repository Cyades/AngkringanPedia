from django.shortcuts import render
from .models import Recipe

def show_main(request):
    context = {
        'name': 'AngkringanPedia'
    }
    return render(request, "main.html", context)

def recipe_list(request):
    recipes = Recipe.objects.all()  # Fetch all recipes from the database
    return render(request, 'recipe_list.html', {'recipes': recipes})
