"""
Run trials on ga and pso algorithms, report on successes and average times
"""

import argparse
import time

from ga import main as genetic_algorithm
from pso import main as particle_swarm_optimization


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--algorithm",
        help="Algorithm",
        type=str,
        default="ga",
        dest="ALGORITHM",
    )
    parser.add_argument(
        "-t",
        "--trials",
        help="Trials",
        type=int,
        default=50,
        dest="TRIALS",
    )

    return parser.parse_args()


def main(args):
    algo = args["ALGORITHM"]
    trials = args["TRIALS"]
    results = []
    times = []

    if algo == "ga":
        for i in range(trials):
            print(f"--- Trial {i+1} ---")
            start = time.time()
            result = genetic_algorithm(
                {
                    "POPULATION_SIZE": 100,
                    "NUMBER_ITERATIONS": 10000,
                    "MUTATION_PCT": 0.5,
                    "BRAKE_ON_SOLUTION": True,
                    "OUTPUT": "none",
                }
            )
            end = time.time()
            results.append(result)
            if result == 1:
                times.append(end - start)

    else:  # pso
        for i in range(trials):
            print(f"--- Trial {i+1} ---")
            start = time.time()
            result = particle_swarm_optimization(
                {
                    "POPULATION_SIZE": 100,
                    "NUMBER_ITERATIONS": 10000,
                    "W": 0.7,
                    "C1": 1,
                    "C2": 1,
                    "OUTPUT": "none",
                }
            )
            end = time.time()
            results.append(result)
            if result == 1:
                times.append(end - start)

    average = sum(times) / len(times)
    success_rate = (results.count(1) / trials) * 100

    print(f"Average time for {algo} after {trials}: {average} seconds")
    print(f"Success rate for {algo} after {trials}: {success_rate} %")


if __name__ == "__main__":
    cli_args = parse_args()

    main(
        {
            "ALGORITHM": cli_args.ALGORITHM,
            "TRIALS": cli_args.TRIALS,
        }
    )
