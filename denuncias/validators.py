import re
from django.core.exceptions import ValidationError


def validar_sin_mayusculas_extremas(value):
    """
    IA: Como validar que un texto no sea spam en mayusculas
    Solucion manual: regex que detecta si >70% son mayusculas
    """
    if not value:
        return
    letras = [c for c in value if c.isalpha()]
    if letras:
        mayusculas = sum(1 for c in letras if c.isupper())
        if (mayusculas / len(letras)) > 0.7:
            raise ValidationError(
                "El texto no puede contener mas del 70% de mayusculas (evite SPAM)."
            )


def validar_no_contiene_scripts(value):
    """
    IA: Como prevenir XSS en campos de texto
    Solucion manual: regex que detecta <script>, javascript:, onerror=
    """
    patrones_peligrosos = [
        r'<script',
        r'javascript:',
        r'onerror\s*=',
        r'onload\s*=',
        r'<iframe',
        r'eval\(',
    ]
    valor_bajo = value.lower() if value else ''
    for patron in patrones_peligrosos:
        if re.search(patron, valor_bajo):
            raise ValidationError(
                f"Contenido no permitido detectado. Elimine codigo malicioso."
            )


def validar_email_institucional(value):
    """
    IA: Como restringir emails a dominios corporativos
    Solucion manual: regex que valida dominio .edu.pe o .gob.pe
    """
    if not value:
        return
    if not re.search(r'@(?:[a-zA-Z0-9-]+\.)+(?:edu\.pe|gob\.pe|org\.pe)$', value):
        raise ValidationError(
            "Use un correo institucional valido (.edu.pe, .gob.pe o .org.pe)."
        )
