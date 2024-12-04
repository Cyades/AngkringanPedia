from django.urls import path
from favorites.views import get_makanan_favorite,delete_favorite,cek_favorit,create_favorite,get_makanan_favorite_admin 

urlpatterns = [
      path('favorites/<int:id_user>/', get_makanan_favorite, name = 'favorites'),
    path('favorites/delete/<int:id_user>/<int:id_makanan>/',delete_favorite, name = 'delete_favorites'),
    path('favorites/create/<int:id_user>/<int:id_makanan>/', create_favorite, name = 'create_favorites'),
    path('favorites/cek_favorit/<int:id_user>/<int:id_makanan>/', cek_favorit, name = 'cek_favorit'),
    path('favorites/admin/<int:id_user>/', get_makanan_favorite_admin, name = 'favorites_admin'),
]