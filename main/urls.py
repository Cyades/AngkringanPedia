from django.urls import path
from main.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('search/', search_recipes, name='search_recipes'),
    path('add-recipe/', add_recipe, name='add_recipe'),
    path('delete/<int:id>', delete_product, name='delete_product'),
    path('api/recipes/', get_recipes, name='get_recipes'),
    path('api/search/', search_recipes_api, name='search_recipes_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)