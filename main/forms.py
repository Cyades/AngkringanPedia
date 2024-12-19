from django import forms
from django.contrib.auth.models import User
from .models import Profile, Recipe, Ingredient
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe, Ingredient
from django import forms

# Form untuk membuat akun baru, termasuk informasi di model User dan Profile
class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])  # Untuk menyimpan password
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


# Form untuk mengedit informasi User (username dan email)
class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


# Form untuk mengedit informasi Profile (nomor telepon dan gambar profil)
class ProfileEditForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False)
    profile_image = forms.ImageField(required=False, widget=forms.FileInput)  # Menghapus ClearableFileInput

    class Meta:
        model = Profile
        fields = ['phone_number', 'profile_image']

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image', None)
        clear = self.data.get('profile_image-clear', False)
        if clear:
            profile_image = None
        return profile_image


# Form untuk menambah resep dengan list bahan dan instruksi
class AddRecipeForm(forms.ModelForm):
    ingredients_list = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter ingredients separated by commas (e.g. flour, sugar, eggs)',
                'rows': 4
            }
        ),
        label='Ingredients',
        required=True  
    )
    instructions = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter cooking instructions',
                'rows': 5
            }
        ),
        label='Instructions',
        required=False
    )

    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cooking_time', 'servings', 'ingredients_list', 'instructions', 'image_url']
        widgets = {
            'recipe_name': forms.TextInput(attrs={'placeholder': 'Enter recipe name'}),
            'cooking_time': forms.TextInput(attrs={'placeholder': 'Enter cooking time (e.g. 30 minutes/1 hour)'}),
            'servings': forms.TextInput(attrs={'placeholder': 'Enter servings (e.g. 4 servings)'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.save()
            ingredients_list = self.cleaned_data['ingredients_list'].split(',')
            for ingredient_name in ingredients_list:
                ingredient_name = ingredient_name.strip()
                if ingredient_name:
                    ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
                    recipe.ingredients.add(ingredient)
            recipe.save()
        return recipe
<<<<<<< HEAD

class CustomUserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    profile_image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['phone_number'].initial = self.instance.profile.phone_number
            self.fields['profile_image'].initial = self.instance.profile.profile_image

    def save(self, commit=True):
        user = super(CustomUserEditForm, self).save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data['phone_number']
            profile.profile_image = self.cleaned_data['profile_image']
            profile.save()
        return user
=======
>>>>>>> 71175b8eb7fbc8ef5928364bc43583c36dfc8898
