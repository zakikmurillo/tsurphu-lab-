import argparse

from engines.tibetan_year import tibetan_year

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="tsurphu")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ty = sub.add_parser(
        "tibetan-year",
        help="Compute Tibetan year attributes for a Gregorian year",
    )
    p_ty.add_argument("year", type=int, help="Gregorian year (e.g., 2025)")

    args = parser.parse_args(argv)

    if args.cmd == "tibetan-year":
        print(tibetan_year(args.year))
        return 0

    # Fallback (should not happen)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
