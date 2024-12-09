from django.urls import path
from . import views

urlpatterns = [
    path('', views.artikel_list, name='artikel_list'),
]
