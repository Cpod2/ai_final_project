"""
Run trials on ga and pso algorithms, average and tabulate results
"""

import argparse
from time import time
import ga
import pso

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
        help=Trials",
        type=int,
        default=50,
        dest="TRIALS",
    )

    return parser.parse_args()
    
def main(args):

    algo = args["ALGORITHM"]
    trials = args["TRIALS"]
    times = []
    
    if algo == "ga":
        for i in range(trials):
            start = time.time()
            cli_args = ga.parse_args()
            ga.main(
                {
                    "POPULATION_SIZE": cli_args.POPULATION_SIZE,
                    "NUMBER_ITERATIONS": cli_args.NUMBER_ITERATIONS,
                    "MUTATION_PCT": cli_args.MUTATION_PCT,
                    "BRAKE_ON_SOLUTION": cli_args.BRAKE_ON_SOLUTION,
                    "OUTPUT": cli_args.OUTPUT,
                }
            )
            end = time.time()
            times.append(end - start)
            
    else: #pso
        for i in range(trials):
            start = time.time()
            cli_args = pso.parse_args()
            pso.main(
                {
                    "POPULATION_SIZE": cli_args.POPULATION_SIZE,
                    "NUMBER_ITERATIONS": cli_args.NUMBER_ITERATIONS,
                    "W": cli_args.W,
                    "C1": cli_args.C1,
                    "C2": cli_args.C2,
                    "OUTPUT": cli_args.OUTPUT,
                }
            )
            end = time.time()
            times.append(end - start)
            
    average = sum(times) / trials
    print(f"average time for {algo} after {trials}: {average}")
    


if __name__ == "__main__":
    cli_args = pso.parse_args()
    
    main(
        {
            "ALGORITHM": cli_args.ALGORITHM,
            "TRIALS": cli_args.TRIALS
        }
    )
