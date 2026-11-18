from django.contrib import admin
from django.utils import timezone
from .models import Denuncia, TipoIrregularidad


@admin.register(TipoIrregularidad)
class TipoIrregularidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    # 1. Campos a mostrar en la lista (list_display)
    list_display = (
        'titulo_corto', 
        'tipo', 
        'estado', 
        'nivel_confidencialidad', 
        'fecha_recepcion', 
        'tiempo_transcurrido' # Campo calculado
    )
    
    # 2. Filtros laterales (list_filter)
    list_filter = ('estado', 'nivel_confidencialidad', 'tipo')
    
    # 3. Barra de búsqueda (search_fields)
    search_fields = ('titulo', 'descripcion', 'denunciante_nombre')
    
    # 4. Campos de solo lectura (readonly_fields)
    readonly_fields = ('fecha_recepcion', 'fecha_actualizacion', 'tiempo_transcurrido')
    
    # Ordenamiento por defecto
    ordering = ('-fecha_recepcion',)

    # 5. Optimización de queries (Requisito de la guía)
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tipo', 'registrado_por')

    # 6. CAMPO CALCULADO 1: Título corto
    @admin.display(description='Título')
    def titulo_corto(self, obj):
        return obj.titulo[:40] + '...' if len(obj.titulo) > 40 else obj.titulo

    # 7. CAMPO CALCULADO 2: Tiempo transcurrido (Requisito de la guía)
    @admin.display(description='Tiempo transcurrido', ordering='fecha_recepcion')
    def tiempo_transcurrido(self, obj):
        delta = timezone.now() - obj.fecha_recepcion
        dias = delta.days
        if dias == 0:
            return "Hoy"
        elif dias == 1:
            return "1 día"
        return f"{dias} días"

    # 8. ACCIÓN MASIVA (Requisito de la guía)
    @admin.action(description='Marcar denuncias seleccionadas como "En investigación"')
    def marcar_en_investigacion(self, request, queryset):
        actualizados = queryset.update(estado='EN_INVESTIGACION')
        self.message_user(request, f'{actualizados} denuncias marcadas como En investigación.')

    # Registrar la acción
    actions = [marcar_en_investigacion]