from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Recipe, RatingReview
from .forms import RatingReviewForm

def create_rating_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = RatingReviewForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        rating_review = form.save(commit=False)
        rating_review.recipe = recipe
        rating_review.save()
        
        # Get the 'next' parameter from the query string
        next_url = request.GET.get('next', '/')
        return HttpResponseRedirect(next_url)

    context = {'form': form, 'recipe': recipe}
    return render(request, "create_rating_review.html", context)


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
