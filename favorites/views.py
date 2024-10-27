from django.http import JsonResponse
from django.shortcuts import render
from .models import Favorite, Recipe
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login')
def create_favorite(request, id_user, id_makanan):
    if request.method == "POST":
        # try:
            user = User.objects.get(pk=id_user)
            recipe = Recipe.objects.get(pk = id_makanan)
        
            existing_favorite = Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).exists()
        
            if existing_favorite:
                return {
                    'status': 'exists',
                    'message': 'Recipe is already in your favorites',
                }
            
            favorite = Favorite.objects.create(
                user=user,
                recipe=recipe
            )
        
            return JsonResponse({
                'status': 'success',
                'message': 'Recipe added to favorites successfully',
                'data': {
                    'favorite_id': favorite.id,
                    'user_id': user.id,
                    'recipe_id': recipe.id
                }
            })
        
        # except Exception as e:
        #     return {
        #         'status': 'error',
        #         'message': f'An error occurred: {str(e)}'
        #     }
@login_required(login_url='/login')
def delete_favorite(request,id_makanan, id_user):
    if request.method == "DELETE":
        try:
            user = User.objects.get(pk=id_user)
            recipe = Recipe.objects.get(pk = id_makanan)
            favorite = Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).first()
            
            if not favorite:
                return {
                    'status': 'not_found',
                    'message': 'Favorite not found for the given user and recipe.'
                }
            favorite.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Favorite deleted succesfully'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            })
@login_required(login_url='/login')
def get_makanan_favorite(request,id_user):
    try:
        user = User.objects.get(pk=id_user)
        favorites = Favorite.objects.filter(user=user)
        return render(request, "favorite.html", {'favoritelist': favorites}) 

    except Exception as e:
        return JsonResponse ({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        })
def cek_favorit(request, id_user, id_makanan):
        if request.method == "GET":
            user = User.objects.get(pk=id_user)
            recipe = Recipe.objects.get(pk = id_makanan)
            favorite = Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).first()
            
            if favorite:
                  return JsonResponse({
                'status': 'success',
                'message': 'Favorite deleted succesfully'
            })
@login_required(login_url='/login')
def get_makanan_favorite_admin(request,id_user):
    try:
        user = User.objects.get(pk=id_user)
        favorites = Favorite.objects.filter(user=user)
        context = {
        'favoritelist': favorites,
        'user' : user
        }
        return render(request, "favorite_admin.html", context) 

    except Exception as e:
        return JsonResponse ({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        })