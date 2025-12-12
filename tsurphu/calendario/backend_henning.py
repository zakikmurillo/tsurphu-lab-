"""
Backend Henning para M2-CAL (esqueleto ampliado con plan de implementación).

Este módulo define la clase HenningBackend, que implementa la interfaz
TibetanCalendarBackend definida en m2_cal, pero por ahora NO realiza
la conversión completa DU_tibetano -> fecha tibetana.

Su objetivo actual es:

- fijar la estructura del backend,
- documentar los pasos que habrá que implementar,
- permitir que el resto del código lo importe sin romper nada.

Más adelante se rellenará con el algoritmo basado en:

- Henning, *Kalachakra and the Tibetan Calendar*,
- Tablas TCG (tcg1309, tcgb1302, RD2018, etc.).

PLAN DE IMPLEMENTACIÓN (mapa de trabajo):

Paso 0 – Convenciones de Tsurphu
--------------------------------
- Usamos el DU_tibetano producido por M2-CAL (ya corregido por amanecer
  local según la propuesta de Henning).
- Trabajamos en primera instancia con la variante "tsurphu", que aplica
  correcciones específicas para Bogotá/local.

Paso 1 – Epoch tibetano de referencia
-------------------------------------
- Elegir una fecha tibetana bien establecida (año/mes/día) y su DU_tibetano
  correspondiente según Henning/TCG.
- Codificarla como constante, por ejemplo::

    EPOCH_TSURPHU = TibetanEpoch(
        name="...",
        du_tibetano=...,
        anio_tibetano=...,
        mes_lunar=...,
        dia_lunar=...,
        notes="...",
    )

- Esta elección de epoch será la base para todos los conteos posteriores.

Paso 2 – Contar días desde el epoch
-----------------------------------
- A partir de un du_tibetano cualquiera, calcular::

    dias_desde_epoch = du_tibetano - EPOCH_TSURPHU.du_tibetano

- Este número (entero o con pequeña fracción) se usará para avanzar o retroceder
  en la secuencia de días lunares tibetanos.

Paso 3 – Modelo de meses y días lunares
---------------------------------------
- Implementar una función interna que, dado dias_desde_epoch, recorra los meses
  tibetanos aplicando las reglas de Henning/TCG para:

  - longitud de los meses (normalmente 29/30 días),
  - inserción de meses bisiestos (duplicados),
  - días repetidos y omitidos.

- Esta función deberá devolver:

    - año tibetano (número absoluto),
    - mes lunar (1–12, con marca de bisiesto),
    - día lunar (1–30),
    - tipo de día (normal, repetido, omitido).

Paso 4 – Capa de 60 años y animales/elementos
--------------------------------------------
- A partir del año tibetano absoluto, calcular:

    - rabjung (ciclo de 60 años),
    - posición dentro del ciclo (1–60),
    - animal del año,
    - elemento del año,
    - género (masculino/femenino) del año.

Paso 5 – Parkha y mewa (futuro)
------------------------------
- Definir funciones auxiliares para calcular parkha y mewa del día y del año
  según las tablas tradicionales.
- Integrar esos resultados en una estructura más completa (por ejemplo,
  un TibetanDateFull) cuando el proyecto lo requiera.

Estado actual: este archivo implementa la estructura mínima y define
un epoch simbólico EPOCH_TSURPHU como marcador de posición. Todas las
secciones anteriores están pendientes de implementación detallada.
"""

from __future__ import annotations

from dataclasses import dataclass

from tsurphu.calendario.m2_cal import TibetanDateBasic, TibetanCalendarBackend


# ---------------------------------------------------------------------------
# Epoch tibetano de referencia (marcador de posición)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TibetanEpoch:
    """
    Epoch tibetano de referencia para conteos relativos.

    Por ahora usamos este dataclass solo como contenedor de datos.
    Los valores concretos se rellenarán cuando extraígamos del material
    de Henning/TCG la fecha exacta a usar.
    """

    name: str
    du_tibetano: float | None
    anio_tibetano: int | None
    mes_lunar: int | None
    dia_lunar: int | None
    notes: str = ""


EPOCH_TSURPHU = TibetanEpoch(
    name="Epoch Tsurphu-Henning (pendiente de fijar)",
    du_tibetano=None,
    anio_tibetano=None,
    mes_lunar=None,
    dia_lunar=None,
    notes=(
        "Este epoch se fijará como la fecha tibetana de referencia usada "
        "por Henning/TCG para el sistema Phugpa/Tsurphu. Pendiente de "
        "cálculo exacto a partir de las tablas TCG y del libro de Henning."
    ),
)


class HenningBackend(TibetanCalendarBackend):
    """
    Backend de calendario tibetano basado en Henning (ESQUELETO).

    ATENCIÓN: esta versión NO implementa todavía las fórmulas tibetanas.
    Simplemente envuelve el DU_tibetano en un TibetanDateBasic sin rellenar
    año/mes/día. Es equivalente a no pasar backend, pero nos fija la interfaz.
    """

    def __init__(self, variante: str = "tsurphu") -> None:
        """
        `variante` permite, en el futuro, cambiar de "escuela" o ajustes:

        - "tsurphu": versión Tsurphu local corregida (Henning + Bogotá).
        - más adelante se podrían añadir otras variantes si es necesario.
        """
        self.variante = variante

    def from_du_tibetano(self, du_tibetano: float) -> TibetanDateBasic:
        """
        Recibe DU_tibetano (float) y devuelve un TibetanDateBasic.

        Versión actual:
        - devuelve solo du_tibetano.
        - deja anio_tibetano, mes_lunar y dia_lunar como None.

        Más adelante aquí irán:
        - el conteo desde un epoch tibetano (EPOCH_TSURPHU),
        - el cálculo de año/mes/día lunar,
        - los días repetidos/omitidos, etc.
        """
        return TibetanDateBasic(du_tibetano=du_tibetano)
