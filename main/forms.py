from django import forms
from .models import Recipe, Ingredient

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cooking_time', 'servings', 'image_url', 'ingredients', 'instructions']
        widgets = {
            'recipe_name': forms.TextInput(attrs={'placeholder': 'Enter recipe name'}),
            'cooking_time': forms.TextInput(attrs={'placeholder': 'Enter cooking time (e.g. 30 minutes)'}),
            'servings': forms.TextInput(attrs={'placeholder': 'Enter servings (e.g. 4 servings)'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
            'ingredients': forms.CheckboxSelectMultiple(),
            'instructions': forms.Textarea(attrs={'placeholder': 'Enter cooking instructions', 'rows': 5}),
        }

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if not servings.isdigit():
            raise forms.ValidationError("Servings should be a number.")
        return servings
