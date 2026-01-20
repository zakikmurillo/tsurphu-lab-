import argparse
import json
from typing import Any, Dict

from engines.tibetan_year import tibetan_year


def _tibetan_year_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Convert the TibetanYear return value into a JSON-serializable dict.
    Works for NamedTuple, dataclass, or plain objects.
    """
    # NamedTuple
    if hasattr(obj, "_asdict"):
        return obj._asdict()  # type: ignore[attr-defined]

    # dataclass
    try:
        import dataclasses

        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
    except Exception:
        pass

    # plain object
    if hasattr(obj, "__dict__"):
        return dict(obj.__dict__)

    # last resort
    return {"value": str(obj)}


def _normalize_tibetan_year_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Canonicalize JSON output for stability in tests and downstream tools.
    """
    element = data.get("element")
    if isinstance(element, str):
        data["element"] = element.lower()
    return data


def cmd_tibetan_year(args: argparse.Namespace) -> int:
    ty = tibetan_year(args.year)

    if args.json:
        data = _normalize_tibetan_year_json(_tibetan_year_to_dict(ty))
        print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(ty)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tsurphu")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ty = sub.add_parser(
        "tibetan-year",
        help="Compute Tibetan year attributes for a Gregorian year",
    )
    p_ty.add_argument("year", type=int, help="Gregorian year (e.g. 2025)")
    p_ty.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of the Python repr",
    )
    p_ty.set_defaults(func=cmd_tibetan_year)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
