from django.db import models
from django.contrib.auth.models import User
from main.models import Recipe
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name = "favorited_by")
    