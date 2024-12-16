from django.db import models

class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    isi = models.TextField()
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='artikel_images/', blank=True, null=True)  # Pastikan ini ada

    def __str__(self):
        return self.judul
