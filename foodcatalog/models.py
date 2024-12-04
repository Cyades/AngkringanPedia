from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from main.models import Recipe
from django.contrib.auth.models import User

class RatingReview(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")  # New user field
    content = models.TextField(blank=True, null=True)
    score = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),  # Batas minimum rating adalah 1
            MaxValueValidator(5)   # Batas maksimum rating adalah 5
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.recipe.recipe_name} by {self.user.username}"