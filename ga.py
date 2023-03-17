"""
Genetic Algorithm to execute a Timing Attack 
on a weak password validation method
"""

import argparse
import random
import time
from typing import List

from matplotlib import pyplot as plt

from auth import validate


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--population-size",
        help="Population size",
        type=int,
        default=100,
        dest="POPULATION_SIZE",
    )
    parser.add_argument(
        "-n",
        "--number-iterations",
        help="Number of Iterations",
        type=int,
        default=10000,
        dest="NUMBER_ITERATIONS",
    )
    parser.add_argument(
        "-m",
        "--mutation-probability",
        help="Mutation Probability",
        type=float,
        default=0.5,
        dest="MUTATION_PCT",
    )
    parser.add_argument(
        "--brake-on-solution",
        help="Stop when a solution is found",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        dest="BRAKE_ON_SOLUTION",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file for plot",
        type=str,
        default="plot",
        dest="OUTPUT",
    )

    return parser.parse_args()


POPULATION_SIZE = 100
NUMBER_ITERATIONS = 10000
MUTATION_PCT = 0.5
BRAKE_ON_SOLUTION = False
OUTPUT = "plot"


def create_population(population_size: int) -> List[str]:
    """
    Returns a population of members.
    Members are strings of 8 digits.
    Allowed digits are 1 to 8.
    The string encodes a password
    candidate.
    """
    return ["".join(random.choices("12345678", k=8)) for _ in range(population_size)]


def calculate_fitness(member: str) -> int:
    """
    Returns a member fitness score
    The fitness score is calculated based on
    the average time it takes for the
    authentication method to validate a member
    of the population.

    A higher average number means our candidate
    is close to the password.
    """
    accumulator = 0
    iterations = 10
    for _ in range(iterations):
        start = time.time_ns()
        validate(member)
        end = time.time_ns()
        accumulator += end - start

    return accumulator / iterations


def select_parents(population: List[str]) -> List[str]:
    """
    Returns parents for next generation with
    their fitness scores.
    Parents are selected from the current
    population proportional to their
    fitness score, using a "normalized
    fitness calculation".
    The method random.choices is used to
    perform this selection, using the fitness
    score as the weights.
    Once the parent for the next generation
    are chosen, their fitness scores are
    calculated and returned as well in the
    result.
    """
    scores = []
    for _, member in enumerate(population):
        scores.append(calculate_fitness(member))
    parents = random.choices(population, weights=scores, k=len(population))
    new_scores = []
    for _, member in enumerate(parents):
        new_scores.append(calculate_fitness(member))
    return (parents, new_scores)


def do_crossover(parent1: str, parent2: str) -> str:
    """
    Return an offspring that is the result
    of the crossover of two parents.
    A random spot is chosen for the crossover.
    The offspring inherits the initial part of
    the first parent, and the last part of the
    second parent.
    """
    cut = random.randint(1, len(parent1))
    return parent1[:cut] + parent2[cut:]


def do_mutation(member: str, pct: float = 0.8) -> str:
    """
    Return a mutated version of member.
    Mutations occur based on a probability
    passed as a parameter (pct).
    A high pct makes mutations more frequent.
    On mutation, a random position in the
    string is selected to be switched to a
    random valid character.
    """
    should_mutate = random.random() > (1 - pct)
    if should_mutate:
        index = random.randint(0, len(member) - 1)
        target = random.choices("12345678", k=1)[0]
        temp = list(member)
        temp[index] = target
        member = "".join(temp)

    return member


def main():
    """
    Main Function.

    The program starts by creating an initial population.
    Then, it executes the genetic algorithm for a fixed
    number of iterations. On each iteration, parents
    for the next generation are selected, and the new
    generation is created based on crossover and
    mutations operations.
    """
    population = create_population(POPULATION_SIZE)
    solution = None
    average = []
    best = []

    print("Initial Population\n")
    for _, member in enumerate(population):
        print(f"Member {member} Fitness {calculate_fitness(member)}")
    print("")

    for _ in range(NUMBER_ITERATIONS):
        # Check if any of the candidates in the next
        # generation is a solution
        for _, candidate in enumerate(population):
            if validate(candidate):
                solution = candidate
                if BRAKE_ON_SOLUTION:
                    break

        parents, scores = select_parents(population)
        average.append(sum(scores) / len(scores))
        best.append(max(scores))
        next_generation = []

        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            score1 = scores[i]
            score2 = scores[i + 1]
            offspring1 = do_crossover(parent1=parent1, parent2=parent2)
            offspring1 = do_mutation(offspring1, MUTATION_PCT)
            next_generation.append(offspring1)
            offspring2 = do_crossover(parent1=parent2, parent2=parent1)
            offspring2 = do_mutation(offspring2, MUTATION_PCT)
            next_generation.append(offspring2)

        population = next_generation

    if solution:
        print("Solution Found\n")
        print(f"Member {solution} Fitness {calculate_fitness(solution)}")
        print("")

    print("Final Population\n")
    for _, member in enumerate(population):
        print(f"Member {member} Fitness {calculate_fitness(member)}")

    plt.plot(average)
    plt.plot(best)
    plt.legend(["Average Fitness", "Best Fitness"])
    plt.title("Fitness Over Population Generation")
    plt.xlabel("Population Generation")
    plt.ylabel("Fitness")
    plt.savefig(OUTPUT)
    plt.show(block=True)


if __name__ == "__main__":
    args = parse_args()
    POPULATION_SIZE = args.POPULATION_SIZE
    NUMBER_ITERATIONS = args.NUMBER_ITERATIONS
    MUTATION_PCT = args.MUTATION_PCT
    BRAKE_ON_SOLUTION = args.BRAKE_ON_SOLUTION
    OUTPUT = args.OUTPUT

    main()
