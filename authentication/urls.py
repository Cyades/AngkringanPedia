from django.urls import path
from main.views import *
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('adminku/', show_admin, name='show_admin'),
    path('adminkudelete/<int:id>', delete_user, name='delete_user'),
    path('get_user_details/<int:user_id>/', get_user_details, name='get_user_details'),
    path('edit-admin/<int:id>', edit_admin, name='edit_admin'),
    path('edit-user/<int:id>/', edit_user, name='edit_user'),
    path('login-flutter/', login_flutter, name='login_flutter'),
    path('logout-flutter/', logout_flutter, name='logout_flutter'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('register-flutter/', register_flutter, name='register_flutter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)