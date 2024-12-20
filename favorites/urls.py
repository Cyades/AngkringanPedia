from django.urls import path
from favorites.views import get_makanan_favorite,delete_favorite,cek_favorit,create_favorite,get_makanan_favorite_admin,cek_favorit_json

app_name = 'favorites'
urlpatterns = [
      path('<int:id_user>/', get_makanan_favorite, name = 'favorites'),
    path('delete/<int:id_user>/<int:id_makanan>/',delete_favorite, name = 'delete_favorites'),
    path('create/<int:id_user>/<int:id_makanan>/', create_favorite, name = 'create_favorites'),
    path('cek_favorit/<int:id_user>/<int:id_makanan>/', cek_favorit, name = 'cek_favorit'),
    path('admin/<int:id_user>/', get_makanan_favorite_admin, name = 'favorites_admin'),
    path('cek_favorit/<int:id_user>/<int:id_makanan>/json/', cek_favorit_json, name = 'cek_favorit_json'),
]