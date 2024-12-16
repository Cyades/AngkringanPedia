# artikel/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Artikel  # Pastikan model Artikel sesuai
from .forms import ArtikelForm  # Pastikan form ArtikelForm sudah dibuat
from django.contrib.auth.decorators import user_passes_test

# Cek apakah user adalah admin
def is_admin(user):
    return user.is_staff or user.is_superuser
# Menampilkan daftar artikel
def show_article_list(request):
    artikel_list = Artikel.objects.all()  # Ambil semua artikel
    return render(request, 'artikel/article_list.html', {'artikel_list': artikel_list})

# Menampilkan detail artikel
def show_article_detail(request, id):
    artikel = get_object_or_404(Artikel, id=id)  # Ambil artikel berdasarkan ID
    return render(request, 'artikel/article_detail.html', {'artikel': artikel})

# Menambahkan artikel (hanya admin)
@user_passes_test(is_admin)
def create_article(request):
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artikel:show_article_list')
    else:
        form = ArtikelForm()
    return render(request, 'artikel/create_article.html', {'form': form})

# Mengedit artikel (hanya admin)
@user_passes_test(is_admin)
def edit_article(request, id):
    artikel = get_object_or_404(Artikel, id=id)
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES, instance=artikel)
        if form.is_valid():
            form.save()
            return redirect('artikel:show_article_detail', id=artikel.id)
    else:
        form = ArtikelForm(instance=artikel)
    return render(request, 'artikel/edit_article.html', {'form': form, 'artikel': artikel})

# Menghapus artikel (hanya admin)
@user_passes_test(is_admin)
def delete_article(request, id):
    artikel = get_object_or_404(Artikel, id=id)
    if request.method == 'POST':
        artikel.delete()
        return redirect('artikel:show_article_list')
    return render(request, 'artikel/delete_article.html', {'artikel': artikel})
