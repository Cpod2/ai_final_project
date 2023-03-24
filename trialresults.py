"""
Run trials on ga and pso algorithms, average and tabulate results
"""

import argparse
import time
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
            start = time.time()
            cli_args = ga.parse_args()
            result = ga.main(
                {
                    "POPULATION_SIZE": cli_args.POPULATION_SIZE,
                    "NUMBER_ITERATIONS": cli_args.NUMBER_ITERATIONS,
                    "MUTATION_PCT": cli_args.MUTATION_PCT,
                    "BRAKE_ON_SOLUTION": cli_args.BRAKE_ON_SOLUTION,
                    "OUTPUT": cli_args.OUTPUT,
                }
            ) 
            end = time.time()
            results.append(result)
            times.append(end - start)
            
    else: #pso
        for i in range(trials):
            start = time.time()
            cli_args = pso.parse_args()
            result = pso.main(
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
            results.append(result)
            times.append(end - start)
            
    average = sum(times) / trials
    success_rate = results.count(1) / trials
    
    print(f"Average time for {algo} after {trials}: {average}")
    print(f"Success rate for {algo} after {trials}: {success_rate} %")
    


if __name__ == "__main__":
    cli_args = parse_args()
    
    main(
        {
            "ALGORITHM": cli_args.ALGORITHM,
            "TRIALS": cli_args.TRIALS,
        }
    )
