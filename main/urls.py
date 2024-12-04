from django.urls import path
from main.views import *
from django.conf import settings
from django.conf.urls.static import static
from favorites.views import get_makanan_favorite, create_favorite, delete_favorite, cek_favorit,get_makanan_favorite_admin
from main.views import edit_user

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('search/', search_recipes, name='search_recipes'),
    path('add-recipe/', add_recipe, name='add_recipe'),
    path('delete/<int:id>/', delete_product, name='delete_product'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('adminku/', show_admin, name='show_admin'),
    path('adminkudelete/<int:id>', delete_user, name='delete_user'),
    path('get_user_details/<int:user_id>/', get_user_details, name='get_user_details'),
    path('edit-admin/<int:id>', edit_admin, name='edit_admin'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('dashboard/', redirect_dashboard, name='redirect_dashboard'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),  # Buat route user_dashboard jika belum ada
    path('edit-user/<int:id>/', edit_user, name='edit_user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
