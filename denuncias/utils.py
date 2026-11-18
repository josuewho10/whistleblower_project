from django.utils.html import escape
import re


def sanitize_input(value, max_length=1000):
    """
    IA: Como sanitizar entradas de usuario antes de persistir
    Solucion manual: strip + escape + normalizacion de espacios
    """
    if not isinstance(value, str):
        return value

    # 1. Eliminar espacios al inicio y final
    value = value.strip()

    # 2. Normalizar espacios multiples a uno solo
    value = re.sub(r'\s+', ' ', value)

    # 3. Limitar longitud
    if len(value) > max_length:
        value = value[:max_length]

    # 4. Escape HTML (previene XSS)
    value = escape(value)

    return value


def sanitize_email(value):
    """Sanitiza y normaliza email a minusculas"""
    if not value:
        return value
    return value.strip().lower()
