# Generated by Django 5.1.1 on 2024-10-26 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='image/default-user.jpg', null=True, upload_to='profile_images/'),
        ),
    ]
