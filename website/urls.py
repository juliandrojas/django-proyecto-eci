from django.urls import path, register_converter
from . import views
from .converters import FileNameConverter

# Registrar el convertidor personalizado
register_converter(FileNameConverter, 'filename')

urlpatterns = [
    path('', views.simple_upload, name='index'),
    path('download/<filename:filename>/', views.download_file, name='download_file'),
    # CRUD CONTACTOS
    path('contact/create/', views.create_user, name='create_user'),
    path('contact/', views.read_user, name='read_user'),
    path('contact/<int:pk>/edit', views.update_user, name='update_user'),
    path('contact/<int:pk>/delete', views.delete_user, name='delete_user'),
]
