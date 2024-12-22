from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    from .models import Profile  # Import di dalam fungsi untuk mencegah import siklik
    if created:
        # Buat profil jika user baru dibuat
        Profile.objects.create(user=instance)
    else:
        # Update profil jika sudah ada
        if not hasattr(instance, 'profile'):  # Cek apakah profil ada
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/default-user.jpg')

    def __str__(self):
        return self.user.username
    

