from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class TipoIrregularidad(models.Model):
    """Categoría de la irregularidad reportada"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tipo de Irregularidad"
        verbose_name_plural = "Tipos de Irregularidad"

    def __str__(self):
        return self.nombre


class NivelConfidencialidad(models.TextChoices):
    ANONIMO = 'ANONIMO', 'Anónimo'
    CONFIDENCIAL = 'CONFIDENCIAL', 'Confidencial'
    PUBLICO = 'PUBLICO', 'Público'


class EstadoDenuncia(models.TextChoices):
    RECIBIDO = 'RECIBIDO', 'Recibido'
    EN_INVESTIGACION = 'EN_INVESTIGACION', 'En investigación'
    RESUELTO = 'RESUELTO', 'Resuelto'
    DESCARTADO = 'DESCARTADO', 'Descartado'


class Denuncia(models.Model):
    """Modelo principal: representa una denuncia"""
    tipo = models.ForeignKey(
        TipoIrregularidad,
        on_delete=models.PROTECT,
        verbose_name="Tipo de irregularidad"
    )
    titulo = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(10, "El título debe tener al menos 10 caracteres")]
    )
    descripcion = models.TextField(
        validators=[MinLengthValidator(50, "La descripción debe tener al menos 50 caracteres")]
    )
    nivel_confidencialidad = models.CharField(
        max_length=20,
        choices=NivelConfidencialidad.choices,
        default=NivelConfidencialidad.ANONIMO
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoDenuncia.choices,
        default=EstadoDenuncia.RECIBIDO
    )
    # Campos opcionales para denuncias NO anónimas
    denunciante_nombre = models.CharField(max_length=100, blank=True, null=True)
    denunciante_email = models.EmailField(blank=True, null=True)
    # Auditoría
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='denuncias_registradas'
    )

    class Meta:
        ordering = ['-fecha_recepcion']
        verbose_name = "Denuncia"
        verbose_name_plural = "Denuncias"

    def __str__(self):
        return f"[{self.get_nivel_confidencialidad_display()}] {self.titulo[:50]}"

    @property
    def es_anonimo(self):
        return self.nivel_confidencialidad == NivelConfidencialidad.ANONIMO