from django.urls import path
from foodcatalog import views

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('/<str:recipe_name>/', views.search_recipe_by_name, name='search_recipe_by_name'),  # URL untuk pencarian resep
]
