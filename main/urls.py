from django.urls import path
from main.views import show_main, search_recipes, add_recipe
from . import views


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('search/', search_recipes, name='search_recipes'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
]


