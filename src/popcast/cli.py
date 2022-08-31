"""Console script for popcast."""
import argparse
import sys

from . import fit, forecast


def main():
    """Console script for popcast."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers()

    fit_parser = subparsers.add_parser("fit")
    fit.register_arguments(fit_parser)
    fit_parser.set_defaults(command=fit)
    fit_parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    forecast_parser = subparsers.add_parser("forecast")
    forecast.register_arguments(forecast_parser)
    forecast_parser.set_defaults(command=forecast)
    forecast_parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    args = parser.parse_args()

    if hasattr(args, "command"):
        args.command.run(args)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
