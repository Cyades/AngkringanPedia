from django.urls import path
from foodcatalog import views

urlpatterns = [
    path('/<str:recipe_name>/', views.search_recipe_by_name, name='search_recipe_by_name'),
    path('/create-rating-review', views.create_rating_review, name='create_rating_review'), # Create rating
    path('/edit-rating-review/<int:review_id>/', views.edit_rating_review, name='edit_rating_review'),  # Edit rating
    path('/delete-rating-review/<int:review_id>/', views.delete_rating_review, name='delete_rating_review'),  # Hapus rating
]

