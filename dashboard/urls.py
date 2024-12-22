from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.show_admin, name='show_admin'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('redirect/', views.redirect_dashboard, name='redirect_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
]
