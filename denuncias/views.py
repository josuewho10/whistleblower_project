from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DenunciaForm, ContactoSoporteForm

def registrar_denuncia(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            # Si el usuario está logueado, guardamos quién lo registró
            if request.user.is_authenticated:
                denuncia.registrado_por = request.user
            denuncia.save()
            messages.success(request, '✅ Denuncia registrada exitosamente.')
            return redirect('denuncia_exito')
        else:
            messages.error(request, '❌ Hubo errores en el formulario. Revíselos abajo.')
    else:
        form = DenunciaForm()

    return render(request, 'denuncias/registrar.html', {'form': form})

def denuncia_exito(request):
    return render(request, 'denuncias/exito.html')

def contacto_soporte(request):
    if request.method == 'POST':
        form = ContactoSoporteForm(request.POST)
        if form.is_valid():
            messages.success(request, '📨 Mensaje enviado al soporte.')
            return redirect('contacto_soporte')
    else:
        form = ContactoSoporteForm()
    return render(request, 'denuncias/contacto.html', {'form': form})
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Vista protegida: solo usuarios autenticados pueden verla"""
    return render(request, 'denuncias/dashboard.html', {'user': request.user})
