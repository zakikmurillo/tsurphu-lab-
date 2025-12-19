from __future__ import annotations

import argparse
import json
from datetime import datetime

from tsurphu.integraciones.stellarium_rc import StellariumRemoteControlClient as C
from tsurphu.astro.coords import equatorial_to_ecliptic, normalize_deg, mean_obliquity_deg


def jd_from_datetime(dt: datetime) -> float:
    # dt.timestamp() is UTC-aware; works with offset-aware datetimes too
    return dt.timestamp() / 86400.0 + 2440587.5


def _float_or_none(x):
    try:
        return None if x is None else float(x)
    except Exception:
        return None


def fetch_body(c: C, name: str, jd: float) -> dict:
    c.focus(name)
    info = c.object_info(name) or {}

    ra = _float_or_none(info.get("ra"))
    dec = _float_or_none(info.get("dec"))

    if ra is None or dec is None:
        raise RuntimeError(f"No RA/Dec for {name}. Got keys: {list(info.keys())}")

    ecl_lon, ecl_lat = equatorial_to_ecliptic(ra, dec, jd)

    out = {
        "ra_deg": ra,
        "dec_deg": dec,
        "ecl_lon_deg": ecl_lon,
        "ecl_lat_deg": ecl_lat,
    }

    # Keep some extras if present
    for k in ("distance", "phase", "mag", "azimuth", "altitude"):
        if k in info:
            out[k] = info.get(k)

    return out


def compute_tithi(moon_lon: float, sun_lon: float) -> dict:
    delta = normalize_deg(moon_lon - sun_lon)  # [0, 360)
    tithi = int(delta // 12.0) + 1             # 1..30
    return {"delta_deg": delta, "tithi": tithi}


def main() -> int:
    ap = argparse.ArgumentParser(description="Ephemeris snapshot via Stellarium RC + ecliptic + tithi.")
    ap.add_argument("--dt", default=None, help="Local datetime ISO with offset, e.g. 1967-03-22T04:44:00-05:00")
    ap.add_argument("--lat", type=float, default=4.7110)
    ap.add_argument("--lon", type=float, default=-74.0721)
    ap.add_argument("--name", default="Bogota")
    ap.add_argument("--country", default="CO")
    args = ap.parse_args()

    dt = datetime.fromisoformat(args.dt) if args.dt else datetime.now().astimezone()
    jd = jd_from_datetime(dt)

    c = C()
    c.set_location(latitude=args.lat, longitude=args.lon, name=args.name, country=args.country)
    c.set_time_jd(jd, 0)  # freeze time

    status = c.status() or {}

    sun = fetch_body(c, "Sun", jd)
    moon = fetch_body(c, "Moon", jd)

    t = compute_tithi(moon["ecl_lon_deg"], sun["ecl_lon_deg"])

    out = {
        "meta": {
            "location": {"name": args.name, "lat": args.lat, "lon": args.lon, "country": args.country},
            "datetime_local": dt.isoformat(),
            "jd": jd,
            "mean_obliquity_deg": mean_obliquity_deg(jd),
        },
        "stellarium_time": status.get("time"),
        "sun": sun,
        "moon": moon,
        "tithi": t,
    }

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
