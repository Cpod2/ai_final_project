"""
Particle Swarm Optimization algorithm to execute a
Timing Attack on a weak password validation method
"""

import argparse
import copy
import random
import time
import numpy as np 
from typing import List
import pyswarm as ps
import statistics

from matplotlib import pyplot as plt

from auth import validate

""""
def calculate_fitness(member: str) -> int:
    
    Returns a member fitness score
    The fitness score is calculated based on
    the average time it takes for the
    authentication method to validate a member
    of the population.

    A higher average number means our candidate
    is close to the password.
    
#    member = str(member)
    accumulator = 0
    iterations = 10
    for _ in range(iterations):
        start = time.time_ns()
        validate(member)
        end = time.time_ns()
        accumulator += end - start

    return accumulator 
"""
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
    iterations = 10
    results = []
    for _ in range(iterations):
        start = time.time_ns()
        validate(member)
        end = time.time_ns()
        results.append(end - start)

    return statistics.median(results)

# Constants
MAX_ITERATIONS = 10000 # need to change
POPULATION_SIZE = 200 # need to change
PASSWORD_LENGTH = 10

# PSO parameters
c1 = 2
c2 = 2
w = 0.7

# Global variables
gbest = None
gbest_fitness = None


class Particle:
    def __init__(self):
        self.position = []    #need to change
        self.velocity = []*10   #need to change
        self.fitness = 0
        self.pbest = [0]*10   #need to change
        self.pbest_fitness = None

        for i in range(PASSWORD_LENGTH):
            self.position.append(random.randint(0, 9))
            self.velocity.append(random.uniform(-1, 1))

    def evaluate_fitness(self):
        password = "".join(str(c) for c in self.position)
        self.fitness = calculate_fitness(password)
        print(self.position,'+',password,':',self.fitness)

        if self.fitness:
#            self.pbest = self.position[:]
            self.pbest = copy.deepcopy(self.position)
            self.pbest_fitness = self.fitness

            global gbest, gbest_fitness
            if gbest_fitness is None or self.pbest_fitness > gbest_fitness:
                gbest = self.pbest[:]
                gbest_fitness = self.pbest_fitness

    def update_velocity(self, gbest):
        for i in range(PASSWORD_LENGTH):
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)
            self.velocity[i] = w * self.velocity[i] + c1 * r1 * (self.pbest[i] - self.position[i]) + c2 * r2 * (gbest[i] - self.position[i])

    def update_position(self):
        for i in range(PASSWORD_LENGTH):
            self.position[i] = int(round(self.position[i] + self.velocity[i]))%10

            # Ensure position is within valid range (0-255)
            self.position[i] = max(self.position[i], 0)
            self.position[i] = min(self.position[i], 255)

    def __str__(self):
        return "".join(chr(c) for c in self.position)


def pso():
    # Initialize particles
    particles = [Particle() for i in range(POPULATION_SIZE)]

    global gbest, gbest_fitness
    gbest = particles[0].position[:]
    gbest_fitness = particles[0].fitness
    
    # Run PSO algorithm
    for iteration in range(MAX_ITERATIONS):
        for particle in particles:
            particle.evaluate_fitness()

        for particle in particles:
            particle.update_velocity(gbest)
            particle.update_position()

        if gbest_fitness == 1:
            break

    # Return best particle found, if any
    if gbest_fitness == 1:
        return "".join(chr(c) for c in gbest)
    else:
        return None

# Test PSO algorithm
target_value = "5555555555"
gbest = None
gbest_fitness = None
print(calculate_fitness("5555555555"))
password = pso()

# Print results
if password is None:
    print("Could not find password.")
else:
    print("Password found:", password)