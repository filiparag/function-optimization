#! /usr/bin/python3

import random
from target_function import target_function
from random import random, randint, uniform
from multiprocessing import Pool
from numpy import arange
import csv
# from scoop import futures


swarm_best, swarm_best_fitness = None, None

class Particle:

    def __init__(self, dim, b_up, b_lo):

        global swarm_best, swarm_best_fitness

        self.position = []

        for i in range(0, dim):
            self.position.append(uniform(b_lo, b_up))

        self.velocity = []

        for i in range(0, dim):
            self.velocity.append(uniform(-abs(b_up - b_lo), abs(b_up - b_lo)))

        self.best = self.position

        if swarm_best is None:
            swarm_best = self.best
            swarm_best_fitness = target_function(self.best)

        elif target_function(self.best) < swarm_best_fitness:
            self.best = swarm_best


def pso(omega, phi, np, dim, it, b_lo, b_up):

    global swarm_best, swarm_best_fitness

    swarm = []

    for p in range(np):
        swarm.append(Particle(dim, b_up, b_lo))

    for i in range(it):

        for particle in swarm:

            for d in range(dim):

                rp, rg = uniform(0, 1), uniform(0, 1)

                particle.velocity[d] = omega * particle.velocity[d] + phi * rp * \
                                       (particle.best[d] - particle.position[d]) + phi \
                                       * rg * (swarm_best[d] - particle.position[d])



            particle.position = [sum(x) for x in zip(particle.position, particle.velocity)]

            if target_function(particle.position) < target_function(particle.best):

                particle.best = particle.position

                if target_function(particle.best) < swarm_best_fitness:

                    swarm_best = particle.best
                    swarm_best_fitness = target_function(swarm_best)

    return swarm_best


def run(params):

    om_range, phi_range, increment_step, repetitions, generation_size,\
    dimensions, iterations, b_lower, b_upper = params

    fitness = []

    omega_vals = [round(x, 6) for x in arange(om_range[0], om_range[1], increment_step).tolist()]
    phi_vals = [round(x, 6) for x in arange(phi_range[0], phi_range[1], increment_step).tolist()]

    for phi in phi_vals:
        for omega in omega_vals:

            average_fitness = 0
            average_position = [0] * dimensions

            for r in range(repetitions):
                position = pso(omega, phi, \
                               generation_size, dimensions, iterations,\
                               b_lower, b_upper)
                average_fitness += target_function(position)
                average_position = [sum(x) for x in zip(average_position, position)]

            average_fitness /= repetitions
            average_position = [x / repetitions for x in average_position]
            fitness.append(average_fitness)

    return fitness


def init():

    cpu_cores = 4
    omega_range = [0, 2]
    phi_range = [0, 3]
    increment_step = 0.01
    repetitions = 1
    generation_size = 4
    dimensions = 2
    iterations = 10000
    b_lower = -2
    b_upper = 2

    worker_tasks = []
    for core in range(cpu_cores):
        worker_tasks.append([
            [
                (core / cpu_cores) * (omega_range[1] - omega_range[0]),
                ((core + 1) / cpu_cores) * (omega_range[1] - omega_range[0]),
            ],
            [
                (core / cpu_cores) * (phi_range[1] - phi_range[0]),
                ((core + 1) / cpu_cores) * (phi_range[1] - phi_range[0]),
            ],
            increment_step,
            repetitions,
            generation_size,
            dimensions,
            iterations,
            b_lower,
            b_upper
        ])

    # single computer
    workers = Pool(cpu_cores)
    worker_results = workers.map(run, worker_tasks)

    # cluster computer
    # worker_results = list(futures.map(run, worker_tasks))

    results = []
    for core in worker_results:
        for result in core:
            results.append(result)

    best_fitness = results[0]
    for r in results:
        if r < best_fitness:
            best_fitness = r

    print(best_fitness)

    with open('results.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        for line in results:
            writer.writerow([line])

if __name__ == '__main__':

    init()