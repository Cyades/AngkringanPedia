from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Recipe, RatingReview
from .forms import RatingReviewForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.http import JsonResponse
from django.db.models import Avg

from django.urls import reverse

@csrf_exempt
def create_rating_review(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        score = request.POST.get('score')
        content = request.POST.get('content', '')  # Default to empty string if not provided

        # Validate that score is provided
        if not score:
            return JsonResponse({'success': False, 'error': 'Rating is required.'})

        # Create the rating review instance
        review = RatingReview.objects.create(
            recipe_id=recipe_id,
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
        }
        return JsonResponse(response_data)

    return JsonResponse({'success': False, 'error': 'Invalid request.'})

def edit_rating_review(request, review_id):
    # Get the review entry based on ID
    review = get_object_or_404(RatingReview, pk=review_id)

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

def delete_rating_review(request, review_id):
    # Get the review based on ID
    review = get_object_or_404(RatingReview, pk=review_id)
    next_url = request.GET.get('next', reverse('main:show_main'))

    if request.method == "POST":
        # Delete the review
        review.delete()
        # Redirect to the main page
        return HttpResponseRedirect(next_url)

    context = {'review': review}
    return render(request, "delete_rating_review.html", context)

def search_recipe_by_name(request, recipe_name):
    # Filter recipes by name
    recipe_name = recipe_name.replace('@', '/')
    recipes = Recipe.objects.filter(recipe_name__iexact=recipe_name)

     # Ambil semua rating review untuk setiap resep
    for recipe in recipes:
        recipe.ratings_list = recipe.ratings.all()  # Mengambil semua rating review terkait

    context = {
        'recipe_name': recipe_name,
        'recipes': recipes,
    }
    return render(request, 'show_recipe.html', context)
