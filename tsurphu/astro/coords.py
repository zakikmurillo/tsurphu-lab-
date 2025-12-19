from __future__ import annotations

import math
from typing import Tuple


def normalize_deg(deg: float) -> float:
    """Normalize degrees to [0, 360)."""
    deg = deg % 360.0
    return deg + 360.0 if deg < 0 else deg


def mean_obliquity_deg(jd: float) -> float:
    """
    Mean obliquity of the ecliptic (degrees).
    IAU 2006 polynomial (good for our purposes).
    """
    T = (jd - 2451545.0) / 36525.0
    eps_arcsec = (
        84381.406
        - 46.836769 * T
        - 0.0001831 * (T ** 2)
        + 0.00200340 * (T ** 3)
        - 5.76e-7 * (T ** 4)
        - 4.34e-8 * (T ** 5)
    )
    return eps_arcsec / 3600.0


def equatorial_to_ecliptic(ra_deg: float, dec_deg: float, jd: float) -> Tuple[float, float]:
    """
    Convert equatorial coordinates (RA/Dec in degrees) to ecliptic lon/lat (degrees)
    using mean obliquity at the given JD.

    NOTE: Assumes Stellarium RC returns RA in degrees (as in your output: ~132 deg).
    """
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    eps = math.radians(mean_obliquity_deg(jd))

    # latitude (beta)
    sin_beta = math.sin(dec) * math.cos(eps) - math.cos(dec) * math.sin(eps) * math.sin(ra)
    sin_beta = max(-1.0, min(1.0, sin_beta))
    beta = math.asin(sin_beta)

    # longitude (lambda)
    y = math.sin(ra) * math.cos(eps) + math.tan(dec) * math.sin(eps)
    x = math.cos(ra)
    lam = math.atan2(y, x)

    lon_deg = normalize_deg(math.degrees(lam))
    lat_deg = math.degrees(beta)
    return lon_deg, lat_deg
