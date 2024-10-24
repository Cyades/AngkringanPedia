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
