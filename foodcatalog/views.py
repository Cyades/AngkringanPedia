from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Recipe, RatingReview
from .forms import RatingReviewForm
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
from django.db.models import Avg

from django.urls import reverse

from foodcatalog.models import RatingReview
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from .models import RatingReview, Recipe

@csrf_exempt
def create_rating_review(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        score = request.POST.get('score')
        content = request.POST.get('content', '')  # Default to empty string if not provided

        # Validate that score is provided
        if not score:
            return JsonResponse({'success': False, 'error': 'Rating is required.'})

        # Check if the user has already rated the recipe
        if RatingReview.objects.filter(recipe_id=recipe_id, user=request.user).exists():
            return JsonResponse({'success': False, 'error': 'You can only rate this recipe once.'})

        # Create the rating review instance
        review = RatingReview.objects.create(
            recipe_id=recipe_id,
            user=request.user,  # Associate the rating with the logged-in user
            score=score,
            content=content
        )

        # Assuming you have a method to calculate the average rating
        average_rating = RatingReview.objects.filter(recipe_id=recipe_id).aggregate(Avg('score'))['score__avg']

        # Prepare response data
        response_data = {
            'success': True,
            'review': {
                'id': review.id,
                'score': review.score,
                'content': review.content,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            },
            'average_rating': average_rating,
            'username':request.user.username,
        }
        return JsonResponse(response_data)

    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required(login_url='/login')
def edit_rating_review(request, review_id):
    # Get the review entry based on ID
    review = get_object_or_404(RatingReview, pk=review_id)

    # Check if the user is the owner of the review or an admin
    if review.user != request.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'You are not authorized to edit this review.'})

    # Set review as an instance of the form
    form = RatingReviewForm(request.POST or None, instance=review)

    next_url = request.GET.get('next', reverse('main:show_main'))

    if request.method == "POST":
        if form.is_valid():
            # Save the form and redirect to the main page
            form.save()
            return HttpResponseRedirect(next_url)

    context = {'form': form, 'review': review}
    return render(request, "edit_rating_review.html", context)


@login_required(login_url='/login')
def delete_rating_review(request, review_id):
    # Get the review based on ID
    review = get_object_or_404(RatingReview, pk=review_id)

    # Check if the user is the owner of the review or an admin
    if review.user != request.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'You are not authorized to delete this review.'})

    next_url = request.GET.get('next', reverse('main:show_main'))

    if request.method == "POST":
        # Delete the review
        review.delete()
        # Redirect to the main page
        return HttpResponseRedirect(next_url)

    context = {'review': review}
    return render(request, "delete_rating_review.html", context)

def show_recipe_by_id(request, recipe_id):
    # Ambil resep berdasarkan ID
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the logged-in user has already rated the recipe
    has_reviewed = RatingReview.objects.filter(recipe=recipe, user=request.user).exists()

    # Ambil semua rating review terkait dengan resep
    recipe.ratings_list = recipe.ratings.all()

    context = {
        'recipe': recipe,  # Kirim data resep tunggal
        'has_reviewed': has_reviewed,
    }
    return render(request, 'show_recipe.html', context)

def show_recipe_json(request, recipe_id):
    # Dapatkan resep berdasarkan ID
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Serialize recipe dan ratings terkait
    data = {
        "id": recipe.id,
        "name": recipe.recipe_name,
        "cooking_time": recipe.cooking_time,
        "servings": recipe.servings,
        "ratings": [
            {
                "id": rating.id,
                "username": rating.user.username,
                "score": rating.score,
                "content": rating.content,
                "created_at": rating.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for rating in recipe.ratings.all()
        ]
    }
    return JsonResponse(data, safe=False)

def show_recipe_xml(request, recipe_id):
    # Dapatkan resep berdasarkan ID
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Serialize recipe dan ratings terkait ke XML
    xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
    <recipe>
        <id>{recipe.id}</id>
        <name>{recipe.recipe_name}</name>
        <cooking_time>{recipe.cooking_time}</cooking_time>
        <servings>{recipe.servings}</servings>
        <ratings>"""
    for rating in recipe.ratings.all():
        xml_data += f"""
            <rating>
                <id>{rating.id}</id>
                <user>{rating.user.username}<user>
                <score>{rating.score}</score>
                <content>{rating.content}</content>
                <created_at>{rating.created_at}</created_at>
            </rating>"""
    xml_data += """
        </ratings>
    </recipe>"""
    return HttpResponse(xml_data, content_type="application/xml")