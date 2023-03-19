"""
Brute Force Algorithm to guess a password 
on a weak password validation method
"""

import argparse

from auth import validate


def parse_args():
    """Parse command line arguments"""
    # pylint: disable=duplicate-code
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--number-iterations",
        help="Number of Iterations",
        type=int,
        default=0,
        dest="NUMBER_ITERATIONS",
    )
    parser.add_argument(
        "--brake-on-solution",
        help="Stop when a solution is found",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        dest="BRAKE_ON_SOLUTION",
    )

    return parser.parse_args()


NUMBER_ITERATIONS = 0
BRAKE_ON_SOLUTION = False


def main(args):
    """
    Main Function.
    """
    solution = None

    # Explore the search space exhaustively
    for i in range(10**10):
        # Each iteration generates a candidate
        # password from 0000000000 to
        # 9999999999. Then it validates the
        # candidate, and checks for early
        # stopping conditions
        candidate = f"{i}".zfill(10)
        if validate(candidate):
            solution = candidate
        if solution and args["BRAKE_ON_SOLUTION"]:
            break
        if args["NUMBER_ITERATIONS"] != 0 and i >= args["NUMBER_ITERATIONS"]:
            break

    # Print the solution
    print(f"Solution = {solution}")


if __name__ == "__main__":
    cli_args = parse_args()

    main(
        {
            "NUMBER_ITERATIONS": cli_args.NUMBER_ITERATIONS,
            "BRAKE_ON_SOLUTION": cli_args.BRAKE_ON_SOLUTION,
        }
    )
