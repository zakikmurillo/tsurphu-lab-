"""Tsurphu ↔ Stellarium (RemoteControl plugin)

Este módulo provee un cliente *muy simple* para hablar con Stellarium a través
del plugin **RemoteControl** (servidor HTTP local, por defecto en el puerto 8090).

¿Por qué existe?
- No queremos "meter" Stellarium dentro de Tsurphu.
- Queremos usarlo como visor/validador externo:
  - fijar tiempo y ubicación
  - consultar estado actual
  - seleccionar/focus de objetos
  - pedir info de objetos

Referencia (RemoteControl API):
- La API está disponible bajo el prefijo `/api/`.
- Ejemplo clave: GET /api/main/status

Nota: Este cliente usa SOLO librería estándar de Python (urllib).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import json
import urllib.parse
import urllib.request


class StellariumRCError(RuntimeError):
    """Error levantado por el cliente de RemoteControl."""


@dataclass(frozen=True)
class StellariumRCConfig:
    host: str = "127.0.0.1"
    port: int = 8090
    timeout_s: float = 2.5

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}".rstrip("/")


class StellariumRemoteControlClient:
    """Cliente HTTP para el plugin RemoteControl de Stellarium."""

    def __init__(self, config: StellariumRCConfig | None = None) -> None:
        self.config = config or StellariumRCConfig()

    # -----------------
    # Bajo nivel
    # -----------------

    def _url(self, path: str) -> str:
        path = "/" + path.lstrip("/")
        return self.config.base_url + path

    def _get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._url(path)
        if params:
            qs = urllib.parse.urlencode({k: str(v) for k, v in params.items()})
            url = url + ("&" if "?" in url else "?") + qs

        req = urllib.request.Request(url=url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout_s) as resp:
                raw = resp.read().decode("utf-8")
        except Exception as e:
            raise StellariumRCError(
                f"No pude conectar con Stellarium RemoteControl en {self.config.base_url}. "
                f"¿Stellarium está abierto y el plugin RemoteControl está activo? Detalle: {e}"
            ) from e

        try:
            return json.loads(raw)
        except Exception as e:
            raise StellariumRCError(f"Respuesta no-JSON desde {url}: {raw[:200]!r}") from e

    def _post_form(self, path: str, data: Dict[str, Any]) -> None:
        """POST con x-www-form-urlencoded (lo que espera el plugin)."""
        url = self._url(path)
        body = urllib.parse.urlencode({k: str(v) for k, v in data.items()}).encode("utf-8")
        req = urllib.request.Request(
            url=url,
            data=body,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout_s) as resp:
                _ = resp.read()
        except Exception as e:
            raise StellariumRCError(f"POST falló hacia {url} con data={data}. Detalle: {e}") from e

    # -----------------
    # Alto nivel
    # -----------------

    def ping(self) -> bool:
        """True si podemos leer /api/main/status."""
        try:
            _ = self.status()
            return True
        except StellariumRCError:
            return False

    def status(self) -> Dict[str, Any]:
        """Estado principal (tiempo, ubicación, vista, selección)."""
        return self._get_json("/api/main/status")

    def set_time_jd(self, jd: float, timerate_jd_per_sec: Optional[float] = None) -> None:
        """Fija el tiempo de simulación.

        - jd: día juliano (ej: 2460000.5)
        - timerate_jd_per_sec: velocidad del tiempo (JDay/sec). Si no se pasa,
          Stellarium conserva la velocidad actual.
        """
        data: Dict[str, Any] = {"time": jd}
        if timerate_jd_per_sec is not None:
            data["timerate"] = timerate_jd_per_sec
        self._post_form("/api/main/time", data)

    def set_location(
        self,
        latitude: float,
        longitude: float,
        altitude_m: float = 0.0,
        name: str = "",
        country: str = "",
        planet: str = "Earth",
    ) -> None:
        """Fija la ubicación del observador.

        Usa: POST /api/location/setlocationfields
        Parámetros: latitude, longitude, altitude, name, country, planet
        """
        self._post_form(
            "/api/location/setlocationfields",
            {
                "latitude": latitude,
                "longitude": longitude,
                "altitude": altitude_m,
                "name": name,
                "country": country,
                "planet": planet,
            },
        )

    def focus(self, target: str, mode: str = "center") -> None:
        """Selecciona/enfoca un objeto por nombre (ej: 'Moon', 'Sun')."""
        self._post_form("/api/main/focus", {"target": target, "mode": mode})

    def object_info(self, name: str, format: str = "json") -> Dict[str, Any]:
        """Información de un objeto del catálogo.

        GET /api/objects/info?format=json&name=Moon
        """
        return self._get_json("/api/objects/info", {"format": format, "name": name})

    def object_find(self, query: str, format: str = "json") -> Dict[str, Any]:
        """Búsqueda por substring.

        GET /api/objects/find?format=json&str=moon
        """
        return self._get_json("/api/objects/find", {"format": format, "str": query})


if __name__ == "__main__":
    cli = StellariumRemoteControlClient()
    st = cli.status()
    print("OK: RemoteControl activo")
    print("Time:", st.get("time"))
    print("Location:", st.get("location"))
