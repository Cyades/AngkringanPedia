# Dalam app2, misalnya di views.py
from main.models import Ingredient, Recipe, Instruction

def show_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})