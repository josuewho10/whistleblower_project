import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class AuditoriaMiddleware:
    """
    IA: Como auditar accesos a rutas sensibles en Django
    Solucion manual: Middleware custom con __init__ y __call__
    que registra en consola el usuario, IP y ruta accedida.
    """
    def __init__(self, get_response):
        # One-time configuration and initialization
        self.get_response = get_response

    def __call__(self, request):
        # Codigo ejecutado ANTES de la vista (request)
        rutas_sensibles = ['/admin/', '/registrar/', '/dashboard/']
        
        if any(request.path.startswith(ruta) for ruta in rutas_sensibles):
            ip = request.META.get('REMOTE_ADDR', 'Desconocida')
            usuario = request.user.username if request.user.is_authenticated else 'Anonimo'
            
            # Log en consola (se vera en la terminal de runserver)
            print(f"[AUDITORIA] {timezone.now().strftime('%H:%M:%S')} | Usuario: {usuario} | IP: {ip} | Ruta: {request.path}")

        response = self.get_response(request)
        
        # Codigo ejecutado DESPUES de la vista (response)
        # Podriamos modificar headers aqui, ej: response['X-Custom-Header'] = 'Value'
        
        return response
