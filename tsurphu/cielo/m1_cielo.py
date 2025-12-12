"""
M1-CIELO – Cielo Tsurphu (versión laboratorio)

Funciones astronómicas básicas para el resto de motores.

Por ahora implementamos:

- to_utc(fecha_local, hora_local, zona)
    Convierte una fecha y hora locales a un objeto datetime en UTC.

- calcular_du(instante_utc)
    Calcula el Día Juliano (Julian Day Number) como base para otros cálculos.
    Esta es una aproximación suficiente para escalas humanas (años/meses/días).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date, time, timezone
from zoneinfo import ZoneInfo
from math import floor


@dataclass
class FechaLocal:
    """Fecha y hora local más zona horaria."""
    fecha: date
    hora: time
    zona: str  # ejemplo: "America/Bogota"


def to_utc(fecha_local: FechaLocal) -> datetime:
    """
    Convierte una FechaLocal a datetime en UTC.

    Ejemplo de uso:
        f = FechaLocal(date(1967, 3, 22), time(4, 44), "America/Bogota")
        instante_utc = to_utc(f)
    """
    tz = ZoneInfo(fecha_local.zona)
    dt_local = datetime.combine(fecha_local.fecha, fecha_local.hora, tzinfo=tz)
    return dt_local.astimezone(timezone.utc)


def calcular_du(instante_utc: datetime) -> float:
    """
    Calcula el Día Juliano (JD) a partir de un instante en UTC.

    Fórmula estándar (Jean Meeus, Astronomical Algorithms).
    El resultado es un número de días (puede tener parte decimal).
    """
    # Aseguramos que está en UTC
    if instante_utc.tzinfo is None:
        instante_utc = instante_utc.replace(tzinfo=timezone.utc)
    else:
        instante_utc = instante_utc.astimezone(timezone.utc)

    año = instante_utc.year
    mes = instante_utc.month
    dia = instante_utc.day
    hora = instante_utc.hour
    minuto = instante_utc.minute
    segundo = instante_utc.second + instante_utc.microsecond / 1_000_000

    # Convertimos la hora a fracción de día
    frac_dia = (hora + (minuto + segundo / 60.0) / 60.0) / 24.0
    d = dia + frac_dia

    if mes <= 2:
        año -= 1
        mes += 12

    A = floor(año / 100)
    B = 2 - A + floor(A / 4)

    jd = floor(365.25 * (año + 4716)) \n        + floor(30.6001 * (mes + 1)) \n        + d + B - 1524.5

    return jd
