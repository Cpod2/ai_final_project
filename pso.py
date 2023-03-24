"""
Particle Swarm Optimization algorithm to execute a
Timing Attack on a weak password validation method
"""

import argparse
import copy
import random
import statistics
import time

from matplotlib import pyplot as plt

from auth import validate


def parse_args():
    """Parse command line arguments"""
    # pylint: disable=duplicate-code
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
        "-w",
        help="Weight",
        type=float,
        default=0.7,
        dest="W",
    )
    parser.add_argument(
        "-c1",
        help="C1",
        type=float,
        default=1,
        dest="C1",
    )
    parser.add_argument(
        "-c2",
        help="C2",
        type=float,
        default=1,
        dest="C2",
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
    iterations = 25
    results = []
    for _ in range(iterations):
        start = time.time_ns()
        validate(member)
        end = time.time_ns()
        results.append(end - start)

    return statistics.median(results)


class Particle:
    def __init__(self):
        self.position = random.randint(0, 10**10 - 1)
        self.velocity = random.uniform(-1, 1)
        self.fitness = 0
        self.pbest = 0
        self.pbest_fitness = 0

    def evaluate_fitness(self, gbest, gbest_fitness):
        password = f"{self.position}".zfill(PASSWORD_LENGTH)
        self.fitness = calculate_fitness(password)

        if self.fitness > self.pbest_fitness:
            self.pbest = copy.deepcopy(self.position)
            self.pbest_fitness = self.fitness

        if self.pbest_fitness > gbest_fitness:
            gbest = copy.deepcopy(self.pbest)
            gbest_fitness = self.pbest_fitness
        return gbest, gbest_fitness

    def update_velocity(self, gbest, w, c1, c2):
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        new_velocity = (
            w * self.velocity
            + c1 * r1 * (self.pbest - self.position)
            + c2 * r2 * (gbest - self.position)
        )
        self.velocity = new_velocity

        return gbest

    def update_position(self):
        self.position = round(self.position + self.velocity)
        self.position = max(self.position, 0)
        self.position = min(self.position, 10**10 - 1)

    def __str__(self):
        password = f"{self.position}".zfill(PASSWORD_LENGTH)
        fitness = self.fitness
        return f"{password} {fitness}"


# Constants
PASSWORD_LENGTH = 10

def pso(POPULATION_SIZE, NUMBER_ITERATIONS, W, C1, C2):
    # Initialize particles
    particles = [Particle() for _ in range(POPULATION_SIZE)]

    average = []
    best = []

    gbest = particles[0].position
    gbest_fitness = particles[0].fitness

    solution = None

    # Run PSO algorithm
    for iteration in range(NUMBER_ITERATIONS):
        for particle in particles:
            gbest, gbest_fitness = particle.evaluate_fitness(gbest, gbest_fitness)

        for particle in particles:
            gbest = particle.update_velocity(gbest, W, C1, C2)
            particle.update_position()
            
        if iteration % 100 == 0:
            fitnesses = [p.fitness for p in particles]
            best.append(max(fitnesses))
            average.append(sum(fitnesses) / len(fitnesses))

        for particle in particles:
            password = f"{particle.position}".zfill(PASSWORD_LENGTH)
            if validate(password):
                solution = particle
                break

        if solution:
            break

    return (password, average, best)


def main(args):
    # Test PSO algorithm
    solution, average, best = pso(
        POPULATION_SIZE=args["POPULATION_SIZE"],
        NUMBER_ITERATIONS=args["NUMBER_ITERATIONS"],
        W=args["W"],
        C1=args["C1"],
        C2=args["C2"],
    )
    
    if args["OUTPUT"] != "none":
        # Print results
        if solution is None:
            print("Could not find password.")
        else:
            print("Solution Found\n")
            print(f"{solution} Fitness {calculate_fitness(solution)}")
            print("")
         
        plt.plot(average)
        plt.plot(best)
        plt.legend(["Average Fitness", "Best Fitness"])
        plt.title("Fitness Over Particle Swarm Movement")
        plt.xlabel("Swarm Iteration")
        plt.ylabel("Fitness")
        plt.savefig(args["OUTPUT"])
        plt.show(block=True)
    
    if solution is None:
        return 0
    else:
        return 1


if __name__ == "__main__":
    cli_args = parse_args()

    main(
        {
            "POPULATION_SIZE": cli_args.POPULATION_SIZE,
            "NUMBER_ITERATIONS": cli_args.NUMBER_ITERATIONS,
            "W": cli_args.W,
            "C1": cli_args.C1,
            "C2": cli_args.C2,
            "OUTPUT": cli_args.OUTPUT,
        }
    )
