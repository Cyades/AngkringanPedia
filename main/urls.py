from django.urls import path
from main.views import *
from django.conf import settings
from django.conf.urls.static import static
from favorites.views import get_makanan_favorite, create_favorite, delete_favorite, cek_favorit

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
    path('favorites/<int:id_user>/', get_makanan_favorite, name = 'favorites'),
    path('favorites/delete/<int:id_user>/<int:id_makanan>/',delete_favorite, name = 'delete_favorites'),
    path('favorites/create/<int:id_user>/<int:id_makanan>/', create_favorite, name = 'create_favorites'),
    path('favorites/cek_favorit/<int:id_user>/<int:id_makanan>/', cek_favorit, name = 'cek_favorit')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
