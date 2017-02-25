#! /usr/bin/python3

import random
from target_function import target_function
from random import random, randint, uniform
from multiprocessing import Pool
from numpy import arange
import csv


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


def pso(params):

    it_s, it_t, np, dim, b_up, b_lo, omega, phi_p, phi_g = params
    
    global swarm_best, swarm_best_fitness

    swarm = []
    results = []

    for p in range(np):
        swarm.append(Particle(dim, b_up, b_lo))

    for i in range(it_t + 1):

        for particle in swarm:

            for d in range(dim):

                rp, rg = uniform(0, 1), uniform(0, 1)

                particle.velocity[d] = omega * particle.velocity[d] + phi_p * rp * \
                                       (particle.best[d] - particle.position[d]) + phi_g \
                                       * rg * (swarm_best[d] - particle.position[d])



            particle.position = [sum(x) for x in zip(particle.position, particle.velocity)]

            if target_function(particle.position) < target_function(particle.best):

                particle.best = particle.position

                if target_function(particle.best) < swarm_best_fitness:

                    swarm_best = particle.best
                    swarm_best_fitness = target_function(swarm_best)

        if i % it_s == 0:
            results.append(swarm_best)

    return results

def init():

    cpu_cores = 4
    omega = 0.729
    phi_p = 2.05
    phi_g = 2.05
    b_lower = 0
    b_upper = 2
    generation_size = 10
    dimensions = 10
    iteration_step = 50
    iteration_target = 1000000
    repetitions = 1

    worker_tasks = [[
        iteration_step,
        iteration_target,
        generation_size,
        dimensions,
        b_upper,
        b_lower,
        omega,
        phi_p,
        phi_g
    ]] * repetitions

    workers = Pool(cpu_cores)
    worker_results = workers.map(pso, worker_tasks)

    results = []
    for i in range(int(iteration_target / iteration_step) + 1):
        iteration_result = [0] * dimensions

        for thread in worker_results:
            iteration_result = [sum(x) for x in zip(iteration_result, thread[i])]

        iteration_result = [x / repetitions for x in iteration_result]
        results.append(iteration_result)

    print(results[-1])

    fitness = [target_function(r) for r in results]
    print(fitness[-1])

    with open('results.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        for line in fitness:
            writer.writerow([line])

if __name__ == '__main__':

    init()