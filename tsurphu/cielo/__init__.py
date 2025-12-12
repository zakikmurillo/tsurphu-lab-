"""
Módulo M1-CIELO (Cielo Tsurphu).

Por ahora solo define la interfaz de alto nivel del motor astronómico:
- calcular_du: día universal (día juliano) para un instante dado.
- to_utc: convertir fecha/hora local + zona horaria a UTC.

Más adelante se añadirá:
- amanecer_local
- posiciones de Sol/Luna/planetas
- info de eclipses, etc.
"""

from .m1_cielo import calcular_du, to_utc
