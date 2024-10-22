from django.urls import path
from main.views import show_main
from .views import recipe_list

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('recipes/', recipe_list, name='recipe_list'), 
]

