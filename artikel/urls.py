# artikel/urls.py

from django.urls import path
from . import views

app_name = 'artikel'

urlpatterns = [
    path('', views.show_article_list, name='show_article_list'),
    path('<int:id>/', views.show_article_detail, name='show_article_detail'),  # URL untuk detail artikel
    path('create/', views.create_article, name='create_article'),  # URL untuk membuat artikel baru
    path('<int:id>/edit/', views.edit_article, name='edit_article'),
    path('<int:id>/delete/', views.delete_article, name='delete_article'),
]
