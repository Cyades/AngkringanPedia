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
    
class CustomUserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']  # Mengambil field dari model User

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        # Isi field dari model Profile jika ada
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['phone_number'].initial = self.instance.profile.phone_number
            self.fields['profile_image'].initial = self.instance.profile.profile_image

    def save(self, commit=True):
        user = super(CustomUserEditForm, self).save(commit=False)
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.phone_number = self.cleaned_data['phone_number']
                profile.profile_image = self.cleaned_data['profile_image']
                profile.save()
        return user