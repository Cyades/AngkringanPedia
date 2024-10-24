from .models import Recipe, Ingredient, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                gender=self.cleaned_data['gender'],
                profile_image=self.cleaned_data['profile_image']
            )
            profile.save()
        return user

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
        fields = ['recipe_name', 'cooking_time', 'servings', 'image_url', 'instructions']
        widgets = {
            'recipe_name': forms.TextInput(attrs={'placeholder': 'Enter recipe name'}),
            'cooking_time': forms.TextInput(attrs={'placeholder': 'Enter cooking time (e.g. 30 minutes)'}),
            'servings': forms.TextInput(attrs={'placeholder': 'Enter servings (e.g. 4 servings)'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Enter cooking instructions', 'rows': 5}),
        }

    def clean_ingredients_list(self):
        ingredients = self.cleaned_data['ingredients_list']
        return [ingredient.strip() for ingredient in ingredients.split(',')]

    def save(self, commit=True):
        recipe = super().save(commit=commit)
        ingredients = self.cleaned_data['ingredients_list']
        for ingredient_name in ingredients:
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
            recipe.ingredients.add(ingredient)
        if commit:
            recipe.save()
        return recipe
