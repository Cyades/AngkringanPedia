from django.urls import path
from .views import user_dashboard, edit_profile, redirect_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('user-dashboard/', user_dashboard, name='user_dashboard'),  # URL untuk dashboard pengguna
    path('edit-profile/', edit_profile, name='edit_profile'),        # URL untuk edit profil
    path('redirect/', redirect_dashboard, name='redirect_dashboard'),  # URL untuk redirect dashboard
]
