from django import forms
from .models import Recipe

class AddRecipeForm(forms.ModelForm):
    ingredients_list = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter ingredients separated by commas (e.g. flour, sugar, eggs)',
                'rows': 4
            }
        ),
        label='Ingredients'
    )
    
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cooking_time', 'servings', 'image_url', 'instructions']  # Exclude 'ingredients' from here
        widgets = {
            'recipe_name': forms.TextInput(attrs={'placeholder': 'Enter recipe name'}),
            'cooking_time': forms.TextInput(attrs={'placeholder': 'Enter cooking time (e.g. 30 minutes)'}),
            'servings': forms.TextInput(attrs={'placeholder': 'Enter servings (e.g. 4 servings)'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Enter cooking instructions', 'rows': 5}),
        }

    def clean_ingredients_list(self):
        ingredients = self.cleaned_data['ingredients_list']
        # Pisahkan ingredients berdasarkan koma, dan buang spasi ekstra
        return [ingredient.strip() for ingredient in ingredients.split(',')]
