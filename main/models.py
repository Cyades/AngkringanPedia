from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    cooking_time = models.CharField(max_length=50)
    servings = models.CharField(max_length=50)
    image_url = models.URLField(max_length=500)
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")
    instructions = models.TextField()

    def __str__(self):
        return self.recipe_name
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.score for rating in ratings) / ratings.count(), 2)
        return None  # Jika belum ada rating

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_instructions")  # Gunakan related_name yang berbeda
    step_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Step {self.step_number} of {self.recipe.recipe_name}"
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # Field Gender
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username
