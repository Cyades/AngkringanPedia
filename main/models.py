from django.db import models

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

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_instructions")  # Gunakan related_name yang berbeda
    step_number = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Step {self.step_number} of {self.recipe.recipe_name}"