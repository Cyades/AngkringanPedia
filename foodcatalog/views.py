import json
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
from xml.etree.ElementTree import Element, SubElement, tostring
from django.utils.encoding import smart_str
from django.contrib.auth.models import User

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

@login_required(login_url='authentication/login')
def edit_rating_review(request, review_id):
    # Get the review entry based on ID
    review = get_object_or_404(RatingReview, pk=review_id)

    # Check if the user is the owner of the review or an admin
    if review.user != request.user and not request.user.is_superuser and not request.user.is_staff:
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


@login_required(login_url='authentication/login')
def delete_rating_review(request, review_id):
    # Get the review based on ID
    review = get_object_or_404(RatingReview, pk=review_id)

    # Check if the user is the owner of the review or an admin
    if review.user != request.user and not request.user.is_superuser and not request.user.is_staff:
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
    
    if (request.user.is_authenticated):
        # Check if the logged-in user has already rated the recipe
        has_reviewed = RatingReview.objects.filter(recipe=recipe, user=request.user).exists()
    else:
        has_reviewed = True

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

    # Cek apakah pengguna telah memberikan ulasan
    has_reviewed = (
        RatingReview.objects.filter(recipe=recipe, user=request.user).exists()
        if request.user.is_authenticated
        else False
    )

    # Serialize recipe, ratings, ingredients, and instructions
    data = {
        "id": recipe.id,
        "name": recipe.recipe_name,
        "image_url": recipe.image_url,
        "cooking_time": recipe.cooking_time,
        "servings": recipe.servings,
        "ingredients": [{"id": ing.id, "name": ing.name} for ing in recipe.ingredients.all()],
        "instructions": [
            {"id": ins.id, "step_number": ins.step_number, "description": ins.description}
            for ins in recipe.recipe_instructions.all().order_by("step_number")
        ],
        "ratings": [
            {
                "id": rating.id,
                "username": rating.user.username,
                "score": rating.score,
                "content": rating.content,
                "created_at": rating.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for rating in recipe.ratings.all()
        ],
        "average_rating": RatingReview.objects.filter(recipe_id=recipe_id).aggregate(Avg('score'))['score__avg'],
        "has_reviewed": has_reviewed,
    }
    return JsonResponse(data, safe=False)

def show_recipe_xml(request, recipe_id):
    # Dapatkan resep berdasarkan ID
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Cek apakah pengguna telah memberikan ulasan
    has_reviewed = (
        RatingReview.objects.filter(recipe=recipe, user=request.user).exists()
        if request.user.is_authenticated
        else False
    )

    # Membuat root XML
    root = Element("recipe")
    SubElement(root, "id").text = str(recipe.id)
    SubElement(root, "name").text = recipe.recipe_name
    SubElement(root, "image_url").text = recipe.image_url or "N/A"
    SubElement(root, "cooking_time").text = str(recipe.cooking_time)
    SubElement(root, "servings").text = str(recipe.servings)
    SubElement(root, "average_rating").text = str(RatingReview.objects.filter(recipe_id=recipe_id).aggregate(Avg('score'))['score__avg'])
    SubElement(root, "has_reviewed").text = str(has_reviewed)

    # Menambahkan ingredients
    ingredients = SubElement(root, "ingredients")
    for ing in recipe.ingredients.all():
        ingredient = SubElement(ingredients, "ingredient")
        SubElement(ingredient, "id").text = str(ing.id)
        SubElement(ingredient, "name").text = ing.name

    # Menambahkan instructions
    instructions = SubElement(root, "instructions")
    for ins in recipe.recipe_instructions.all().order_by("step_number"):
        instruction = SubElement(instructions, "instruction")
        SubElement(instruction, "id").text = str(ins.id)
        SubElement(instruction, "step_number").text = str(ins.step_number)
        SubElement(instruction, "description").text = ins.description

    # Menambahkan ratings
    ratings = SubElement(root, "ratings")
    for rating in recipe.ratings.all():
        rating_elem = SubElement(ratings, "rating")
        SubElement(rating_elem, "id").text = str(rating.id)
        SubElement(rating_elem, "username").text = rating.user.username
        SubElement(rating_elem, "score").text = str(rating.score)
        SubElement(rating_elem, "content").text = smart_str(rating.content)
        SubElement(rating_elem, "created_at").text = rating.created_at.strftime('%Y-%m-%d %H:%M:%S')

    # Serialisasi XML ke string
    xml_data = tostring(root, encoding="utf-8", method="xml")
    return HttpResponse(xml_data, content_type="application/xml")

@csrf_exempt
def create_rating_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        review = RatingReview.objects.create(
            user=user,
            recipe_id=data["recipe_id"],
            score=int(data["score"]),
            content=data.get("content", "")
        )
        review.save()
        return JsonResponse({"status": "success", "review_id": review.id}, status=200)
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def edit_rating_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:  
            # Cari review berdasarkan review_id
            review = get_object_or_404(RatingReview, pk=data['review_id'])
            
            # Update fields review
            review.score = int(data.get("score", review.score))
            review.content = data.get("content", review.content)
            review.save()

            return JsonResponse({"status": "success"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        except RatingReview.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found"}, status=404)
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def delete_rating_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            # Cari review berdasarkan review_id
            review = get_object_or_404(RatingReview, pk=data['review_id'])
            
            # Hapus review
            review.delete()
            return JsonResponse({"status": "success"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        except RatingReview.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found"}, status=404)
    return JsonResponse({"status": "error"}, status=401)