from django import forms
from django.core.exceptions import ValidationError
from .models import Denuncia, NivelConfidencialidad
from .validators import (
    validar_sin_mayusculas_extremas,
    validar_no_contiene_scripts,
    validar_email_institucional,
)
from .utils import sanitize_input, sanitize_email


class DenunciaForm(forms.ModelForm):
    """ModelForm con validacion en 3 niveles"""

    class Meta:
        model = Denuncia
        fields = [
            'tipo', 'titulo', 'descripcion',
            'nivel_confidencialidad',
            'denunciante_nombre', 'denunciante_email'
        ]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Irregularidades en licitacion'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describa los hechos (minimo 50 caracteres)...'
            }),
            'nivel_confidencialidad': forms.Select(attrs={'class': 'form-select'}),
            'denunciante_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional si es anonimo'
            }),
            'denunciante_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional si es anonimo'
            }),
        }

    # ============================================
    # NIVEL 1: Validadores en el campo (regex)
    # ============================================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].validators.append(validar_sin_mayusculas_extremas)
        self.fields['descripcion'].validators.append(validar_no_contiene_scripts)

    # ============================================
    # NIVEL 2: clean_<campo>() por cada campo
    # ============================================
    def clean_titulo(self):
        """Sanitizacion del titulo"""
        titulo = self.cleaned_data.get('titulo', '')
        titulo = sanitize_input(titulo, max_length=150)
        return titulo

    def clean_descripcion(self):
        """Sanitizacion + validacion de contenido"""
        descripcion = self.cleaned_data.get('descripcion', '')
        descripcion = sanitize_input(descripcion, max_length=5000)

        if len(descripcion) < 50:
            raise ValidationError(
                "La descripcion debe tener al menos 50 caracteres."
            )
        return descripcion

    def clean_denunciante_email(self):
        """Validar formato y normalizar"""
        email = self.cleaned_data.get('denunciante_email', '')
        if email:
            email = sanitize_email(email)
            validar_email_institucional(email)
        return email

    def clean_denunciante_nombre(self):
        """Normalizar nombre"""
        nombre = self.cleaned_data.get('denunciante_nombre', '')
        if nombre:
            nombre = sanitize_input(nombre, max_length=100)
        return nombre

    # ============================================
    # NIVEL 3: clean() cross-field
    # ============================================
    def clean(self):
        """
        IA: Como validar que campos dependan entre si
        Solucion manual: clean() revisa cleaned_data global
        """
        cleaned_data = super().clean()
        confidencialidad = cleaned_data.get('nivel_confidencialidad')
        nombre = cleaned_data.get('denunciante_nombre')
        email = cleaned_data.get('denunciante_email')

        # Regla: si es ANONIMO, no debe haber datos personales
        if confidencialidad == NivelConfidencialidad.ANONIMO:
            if nombre or email:
                # add_error permite errores no fatales por campo
                self.add_error('denunciante_nombre',
                    'No puede llenar nombre en denuncia anonima.')
                self.add_error('denunciante_email',
                    'No puede llenar email en denuncia anonima.')

        # Regla: si es CONFIDENCIAL o PUBLICO, email es obligatorio
        if confidencialidad in [
            NivelConfidencialidad.CONFIDENCIAL,
            NivelConfidencialidad.PUBLICO
        ]:
            if not email:
                self.add_error('denunciante_email',
                    'Email obligatorio para denuncias no anonimas.')

        return cleaned_data


class ContactoSoporteForm(forms.Form):
    """Formulario clasico con validacion"""
    asunto = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    email_contacto = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    acepta_terminos = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Debe aceptar los terminos'}
    )

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        if len(mensaje) < 20:
            raise ValidationError("El mensaje es muy corto (minimo 20 caracteres)")
        return sanitize_input(mensaje)

    def clean_email_contacto(self):
        return sanitize_email(self.cleaned_data.get('email_contacto', ''))
