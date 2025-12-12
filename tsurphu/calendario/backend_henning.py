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

PLAN DE IMPLEMENTACIÓN (mapa de trabajo, RESUMEN):

- Paso 0: Convenciones de Tsurphu (ya fijadas en M1/M2).
- Paso 1: Epoch tibetano EPOCH_TSURPHU.
- Paso 2: dias_desde_epoch = du_tibetano - EPOCH_TSURPHU.du_tibetano.
- Paso 3: Resolver año/mes/día lunar a partir de dias_desde_epoch.
- Paso 4: Añadir ciclo de 60 años, animales y elementos (más adelante).
- Paso 5: Añadir parkha y mewa (más adelante).

CANDIDATO A EPOCH_TSURPHU (nota de trabajo):
- Aquí anotaremos, en comentarios, la fecha tibetana concreta que tomaremos
  como epoch de referencia una vez hayamos identificado en Henning/TCG una
  fecha especialmente estable y tradicional (por ejemplo, un año nuevo
  tibetano bien documentado en el sistema Phugpa/Tsurphu).
- Hasta entonces, EPOCH_TSURPHU mantiene todos sus campos numéricos a None.

Estado actual: este archivo define la estructura mínima, un epoch simbólico
EPOCH_TSURPHU, y el esqueleto de funciones internas para el conteo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from tsurphu.calendario.m2_cal import TibetanDateBasic, TibetanCalendarBackend


# ---------------------------------------------------------------------------
# Epoch tibetano de referencia (marcador de posición)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TibetanEpoch:
    """Epoch tibetano de referencia para conteos relativos.

    Por ahora usamos este dataclass solo como contenedor de datos.
    Los valores concretos se rellenarán cuando extraigamos del material
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


# ---------------------------------------------------------------------------
# Backend Henning: estructura y funciones internas (esqueleto)
# ---------------------------------------------------------------------------


class HenningBackend(TibetanCalendarBackend):
    """Backend de calendario tibetano basado en Henning (ESQUELETO).

    ATENCIÓN: esta versión NO implementa todavía las fórmulas tibetanas.
    De momento, envuelve el DU_tibetano en un TibetanDateBasic con campos
    de año/mes/día aún vacíos.
    """

    def __init__(self, variante: str = "tsurphu") -> None:
        """`variante` permitirá en el futuro distinguir ajustes de escuela.

        - "tsurphu": versión Tsurphu local corregida (Henning + Bogotá).
        - Más variantes se pueden añadir más adelante.
        """
        self.variante = variante

    # --------------------------
    # Funciones internas (esqueleto)
    # --------------------------

    def _dias_desde_epoch(self, du_tibetano: float) -> float:
        """Calcula los días (reales) transcurridos desde EPOCH_TSURPHU.

        Cuando EPOCH_TSURPHU.du_tibetano sea un número real, la fórmula será:

            dias = du_tibetano - EPOCH_TSURPHU.du_tibetano

        Por ahora, como el epoch aún no está fijado (du_tibetano=None),
        devolvemos simplemente 0.0 y dejamos documentado el lugar donde
        irá la lógica real.
        """
        if EPOCH_TSURPHU.du_tibetano is None:
            return 0.0

        return du_tibetano - EPOCH_TSURPHU.du_tibetano

    def _resolver_anio_mes_dia(self, dias_desde_epoch: float) -> Tuple[int, int, int]:
        """Resuelve (año tibetano, mes lunar, día lunar) a partir de
        `dias_desde_epoch`.

        Versión actual (esqueleto): devuelve siempre (0, 0, 0).

        Más adelante aquí se implementará:
        - el avance/retroceso mes a mes según las tablas de Henning/TCG,
        - el tratamiento de meses bisiestos (duplicados),
        - el tratamiento de días repetidos y omitidos.
        """
        return 0, 0, 0

    # --------------------------
    # Interfaz pública requerida por TibetanCalendarBackend
    # --------------------------

    def from_du_tibetano(self, du_tibetano: float) -> TibetanDateBasic:
        """Recibe DU_tibetano (float) y devuelve un TibetanDateBasic.

        Versión actual:
        - calcula dias_desde_epoch (aunque todavía sin epoch real),
        - llama a _resolver_anio_mes_dia (que ahora devuelve (0, 0, 0)),
        - devuelve un TibetanDateBasic con du_tibetano y campos de año/mes/día
          todavía sin contenido real.

        Cuando el algoritmo Henning esté implementado, esta función será
        la puerta de entrada para obtener la fecha tibetana completa.
        """
        dias_desde_epoch = self._dias_desde_epoch(du_tibetano)
        anio, mes, dia = self._resolver_anio_mes_dia(dias_desde_epoch)

        return TibetanDateBasic(
            du_tibetano=du_tibetano,
            anio_tibetano=anio if anio != 0 else None,
            mes_lunar=mes if mes != 0 else None,
            dia_lunar=dia if dia != 0 else None,
        )
