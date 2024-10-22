from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'AngkringanPedia'
    }
    return render(request, "main.html", context)