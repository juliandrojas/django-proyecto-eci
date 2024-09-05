from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Upload, User
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse, Http404
import os
from urllib.parse import unquote
from .forms import UserForm
def index_eci(request): 
    visible_users = User.objects.filter(visible=True)
    return render(request, 'index.html', {'users': visible_users})
def simple_upload(request):
    if request.method == 'POST':
        myfile = request.FILES.get('myfile')
        
        if myfile and myfile.name:
            if Upload.objects.filter(file_name=myfile.name).exists():
                messages.error(request, "El archivo ya ha sido subido.")
                return redirect('index')

            fs = FileSystemStorage()
            if fs.exists(myfile.name):
                messages.error(request, "El archivo ya existe en el sistema de archivos.")
                return redirect('index')
            
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            
            upload = Upload(file_name=myfile.name, file_path=uploaded_file_url)
            upload.save()
            
            messages.success(request, "Archivo subido exitosamente.")
            return redirect('index')
        else:
            messages.error(request, "No se ha subido un archivo válido.")
            return redirect('index')
    
    uploads = Upload.objects.all()
    return render(request, 'index.html', {'uploads': uploads})

def download_file(request, filename):
    # Decodificar el nombre del archivo para manejar caracteres especiales correctamente
    filename = unquote(filename)
    
    # Seguridad: Limitar la ruta para evitar Path Traversal
    if '..' in filename or filename.startswith('/'):
        return HttpResponseBadRequest("Nombre de archivo no válido.")
    
    # Construir la ruta completa del archivo en el sistema de archivos
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    
    # Verificar si el archivo existe y manejar la descarga
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            # Agregar el encabezado para la descarga de archivos
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    
    # Si el archivo no se encuentra, lanzar un error 404
    raise Http404("El archivo no existe.")

# Create User
def create_user(request):
    if request.method == 'POST':
        # Almacenamos la información que viene del método POST
        form = UserForm(request.POST)
        # Si la información del usuario es válida
        if form.is_valid():
            # Guardamos el usuario
            form.save()
            # Redireccionamos a la página principal
            return redirect('read_user')
    else:
        # Si el método no es POST, creamos un formulario vacío
        form = UserForm()
    return render(request, 'user/form_user.html', { 'form' : form })
def read_user(request):
    users = User.objects.all()
    return render(request, 'user/list_user.html', { 'users' : users })
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        # Si la información del usuario es válida
        if form.is_valid():
            # Guardamos el usuario
            form.save()
            # Redireccionamos a la página principal
            return redirect('read_user')
    else:
        # Si no es método POST, mandamos el formulario vacío
        form = UserForm(instance=user)
    return render(request, 'user/form_user.html', {'form': form})
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('read_user')
    return render(request, 'user/confirm_delete.html', { 'user': user })