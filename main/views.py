from django.shortcuts import render
from .models import Recipe


def show_main(request):
    # Jika pengguna tidak login, atur 'last_login' ke None atau pesan default
    last_login = request.COOKIES.get('last_login', 'Guest User')

    context = {
        'name': 'AngkringanPedia',
        'recipes': Recipe.objects.all(),
        'last_login': last_login,
    }
    return render(request, "main.html", context)