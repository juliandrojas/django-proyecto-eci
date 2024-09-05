from django.db import models
import os

class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)
    img_category = models.ImageField(upload_to='categories', null=True)

    def __str__(self):
        return self.name

class Upload(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='uploads', null=True)

    def __str__(self):
        return f'Archivo: {self.file_name}'

    @property
    def filename(self):
        return os.path.basename(self.file_path).split('.')[0]

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    orcid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    visible = models.BooleanField(default=True)
    img_profile_path = models.ImageField(upload_to='profile', null=True)

    def __str__(self):
        return 'Usuario: ' + self.username

    def __str__(self):
        return 'Usuario: ' + self.username
