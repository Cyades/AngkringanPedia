from django.contrib import admin
from .models import Recipe  
from favorites.models import Favorite
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_name', 'cooking_time', 'servings') 

admin.site.register(Recipe, RecipeAdmin) 
admin.site.register(Favorite)
