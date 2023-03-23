"""
Particle Swarm Optimization algorithm to execute a
Timing Attack on a weak password validation method
"""

import argparse
import copy
import random
import statistics
import time

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

    def evaluate_fitness(self):
        password = f"{self.position}".zfill(PASSWORD_LENGTH)
        self.fitness = calculate_fitness(password)

        if self.fitness > self.pbest_fitness:
            self.pbest = copy.deepcopy(self.position)
            self.pbest_fitness = self.fitness

        global gbest, gbest_fitness
        if self.pbest_fitness > gbest_fitness:
            gbest = copy.deepcopy(self.pbest)
            gbest_fitness = self.pbest_fitness

    def update_velocity(self, gbest):
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        new_velocity = (
            W * self.velocity
            + C1 * r1 * (self.pbest - self.position)
            + C2 * r2 * (gbest - self.position)
        )
        self.velocity = new_velocity

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

# PSO parameters
C1 = 2
C2 = 2
W = 0.7


def pso(POPULATION_SIZE, NUMBER_ITERATIONS):
    # Initialize particles
    particles = [Particle() for _ in range(POPULATION_SIZE)]

    global gbest, gbest_fitness
    gbest = particles[0].position
    gbest_fitness = particles[0].fitness

    solution = None

    # Run PSO algorithm
    for iteration in range(NUMBER_ITERATIONS):
        for particle in particles:
            particle.evaluate_fitness()

        for particle in particles:
            particle.update_velocity(gbest)
            particle.update_position()

        if iteration % 500 == 0:
            print(f"[{iteration}] {gbest} = {gbest_fitness}")

        for particle in particles:
            password = f"{particle.position}".zfill(PASSWORD_LENGTH)
            if validate(password):
                solution = particle
                break

        if solution:
            break

    return solution


def main(args):
    # Global variables
    gbest = 0
    gbest_fitness = 0

    # Test PSO algorithm
    password = pso(
        POPULATION_SIZE=args["POPULATION_SIZE"],
        NUMBER_ITERATIONS=args["NUMBER_ITERATIONS"],
    )

    # Print results
    if password is None:
        print("Could not find password.")
    else:
        print("Password found:", password)


if __name__ == "__main__":
    cli_args = parse_args()

    main(
        {
            "POPULATION_SIZE": cli_args.POPULATION_SIZE,
            "NUMBER_ITERATIONS": cli_args.NUMBER_ITERATIONS,
        }
    )
