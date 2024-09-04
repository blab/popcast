"""Compare TSV files line by line with deepdiff
"""
import argparse
import deepdiff
import pandas as pd


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare TSV files line by line with deepdiff",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("first_tsv", help="first TSV to compare")
    parser.add_argument("second_tsv", help="second TSV to compare")
    parser.add_argument("--significant-digits", type=int, default=6, help="number of significant digits to use when comparing numeric values")

    args = parser.parse_args()

    first_tsv = pd.read_csv(
        args.first_tsv,
        sep="\t",
        header=None,
        engine="python",
        na_filter=False,
    ).to_dict()

    second_tsv = pd.read_csv(
        args.second_tsv,
        sep="\t",
        header=None,
        engine="python",
        na_filter=False,
    ).to_dict()

    print(
        deepdiff.DeepDiff(
            first_tsv,
            second_tsv,
            significant_digits=args.significant_digits,
        )
    )
