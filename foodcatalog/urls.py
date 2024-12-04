from django.urls import path
from foodcatalog import views

urlpatterns = [
    path('<int:recipe_id>/', views.show_recipe_by_id, name='show_recipe_by_id'),
    path('create-rating-review', views.create_rating_review, name='create_rating_review'), # Create rating
    path('edit-rating-review/<int:review_id>/', views.edit_rating_review, name='edit_rating_review'),  # Edit rating
    path('delete-rating-review/<int:review_id>/', views.delete_rating_review, name='delete_rating_review'),  # Hapus rating
    path('<int:recipe_id>/json', views.show_recipe_json, name='show_recipe_json'),
    path('<int:recipe_id>/xml', views.show_recipe_xml, name='show_recipe_xml'),
    path('flutter/create/', views.create_rating_review_flutter, name='create_rating_review_flutter'),
    path('flutter/edit/<int:review_id>/', views.edit_rating_review_flutter, name='edit_rating_review_flutter'),
    path('flutter/delete/<int:review_id>/', views.delete_rating_review_flutter, name='delete_rating_review_flutter'),
]

