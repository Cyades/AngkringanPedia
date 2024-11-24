import json
from django.core.management.base import BaseCommand
from homepage.models import Recipe, Ingredient, Instruction

class Command(BaseCommand):
    help = 'Load recipes from dataset.json'

    def handle(self, *args, **kwargs):
        with open('dataset.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        recipes_data = data.get("dataset", [])
        if not isinstance(recipes_data, list):
            self.stdout.write(self.style.ERROR("Dataset JSON tidak memiliki format yang benar."))
            return

        for recipe_data in recipes_data:
            if not isinstance(recipe_data, dict):
                self.stdout.write(self.style.ERROR("Data resep tidak valid, harus berupa dictionary."))
                continue
            
            recipe_name = recipe_data.get('recipe_name', None)
            cooking_time = recipe_data.get('cooking_time', None)

            if recipe_name is None:
                self.stdout.write(self.style.ERROR("Skipping recipe due to missing recipe_name."))
                continue
            
            if cooking_time is None or not cooking_time.strip():
                self.stdout.write(self.style.ERROR(f"Skipping recipe {recipe_name} due to missing cooking_time."))
                continue

            recipe = Recipe.objects.create(
                recipe_name=recipe_name,
                cooking_time=cooking_time.strip(),
                servings=recipe_data.get('servings', ''),
                image_url=recipe_data.get('image_url', ''),
                instructions="" 
            )

            for ingredient_name in recipe_data.get('ingredients', []):
                ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name.strip())
                recipe.ingredients.add(ingredient)

            for instr_data in recipe_data.get('instructions', []):
                if 'step_number' in instr_data and 'description' in instr_data:
                    Instruction.objects.create(
                        recipe=recipe,
                        step_number=instr_data['step_number'],
                        description=instr_data['description']
                    )
                else:
                    self.stdout.write(self.style.ERROR(f"Invalid instruction format for recipe {recipe_name}."))

        self.stdout.write(self.style.SUCCESS('Successfully loaded recipes into the database.'))
