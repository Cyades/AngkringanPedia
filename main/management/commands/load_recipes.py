import json
from django.core.management.base import BaseCommand
from main.models import Recipe, Ingredient, Instruction

class Command(BaseCommand):
    help = 'Load recipes from dataset.json'

    def handle(self, *args, **kwargs):
        # Buka file dataset.json
        with open('dataset.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for recipe_data in data:
            # Validasi cooking_time agar tidak None atau kosong
            cooking_time = recipe_data.get('cooking_time', '').strip()
            if not cooking_time:
                self.stdout.write(self.style.ERROR(f"Skipping recipe {recipe_data['recipe_name']} due to missing cooking_time."))
                continue

            # Buat objek Recipe tanpa instruksi (instruksi akan ditambahkan secara terpisah)
            recipe = Recipe.objects.create(
                recipe_name=recipe_data['recipe_name'],
                cooking_time=cooking_time,  # Pastikan cooking_time ada
                servings=recipe_data['servings'],
                image_url=recipe_data['image_url'],
                instructions=""  # Ini akan diisi dengan instruksi dari JSON di langkah berikut
            )

            # Tambahkan bahan ke Recipe
            for ingredient_name in recipe_data['ingredients']:
                ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
                recipe.ingredients.add(ingredient)

            # Tambahkan instruksi ke Recipe
            instructions_text = []
            for instr_data in recipe_data['instructions']:
                # Buat setiap instruksi terkait
                instruction = Instruction.objects.create(
                    recipe=recipe,
                    step_number=instr_data['step_number'],
                    description=instr_data['description']
                )
                # Tambahkan deskripsi instruksi ke dalam daftar untuk disimpan sebagai teks
                instructions_text.append(f"Step {instr_data['step_number']}: {instr_data['description']}")

            # Gabungkan semua instruksi menjadi satu teks panjang dan simpan ke field `instructions`
            recipe.instructions = "\n".join(instructions_text)
            recipe.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded recipes into the database.'))
