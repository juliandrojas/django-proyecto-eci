from django.db import models

# Create your models here.

class Upload(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255, blank=True, null=True, default='No registrado')
    orcid = models.CharField(max_length=255, unique=True, blank=True, null=True, default='No registrado')
    visible = models.BooleanField(default=True)

