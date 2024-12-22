# artikel/urls.py

from django.urls import path
from . import views
from django.contrib.auth.decorators import user_passes_test
from .views import create_article, edit_article, delete_article, is_admin

app_name = 'artikel'

urlpatterns = [
    path('', views.show_article_list, name='show_article_list'),
    path('<int:id>/', views.show_article_detail, name='show_article_detail'),  # URL untuk detail artikel
    path('create/', user_passes_test(is_admin)(create_article), name='create_article'),
    path('<int:id>/edit/', user_passes_test(is_admin)(edit_article), name='edit_article'),
    path('<int:id>/delete/', user_passes_test(is_admin)(delete_article), name='delete_article'),
]
