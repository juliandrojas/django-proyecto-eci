from django.contrib import admin
from .models import User, Upload, Categories
# Register your models here.
admin.site.register(User)
admin.site.register(Upload)
admin.site.register(Categories)