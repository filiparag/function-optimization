#! /usr/bin/python3

from random import random, randint
from math import sqrt, exp, cos
from multiprocessing import Pool
from numpy import arange
import csv

def target_function(params):

    result = -20 * exp(-0.2 * sqrt(0.5 * (params[0] ** 2 + params[1] ** 2))) - \
             exp(0.5 * (cos(6.2 * params[0]) + cos(6.2 * params[1]))) + 2.71 + 20

    # Beale
    # result = (1.5 - params[0] + params[0] * params[1]) ** 2 + (2.25 - params[0] \
    #          + params[0] * (params[1] ** 2)) ** 2 + \
    #          (2.625 - params[0] + params[0] * (params[1] ** 3)) ** 2

    # Rosenbrock
    # result = 0
    # for i in range(len(params) - 1):
    #     result += 100 * (params[i + 1] - params[i] ** 2) ** 2 + (params[i] - 1) ** 2

    return result

def differential_evolution(cr, f, np, dim, it, b_lo=-1, b_up=1):

    agents = [[(random() * (b_up - b_lo)) for x in range(dim)] for a in range(np)]

    for i in range(it):
        for x in range(np):

            a, b, c = randint(0, np - 1), randint(0, np - 1), randint(0, np - 1)
            while a == b or b == c or c == a or a == x or b == x or c == x:
                a, b, c = randint(0, np - 1), randint(0, np - 1), randint(0, np - 1)

            R = randint(0, dim)
            y = [None] * dim

            for i in range(dim):
                ri = random()
                if ri < cr or i == R:
                    y[i] = agents[a][i] + f * (agents[b][i] - agents[c][i])
                else:
                    y[i] = agents[x][i]

            if target_function(y) < target_function(agents[x]):
                agents[x] = y

    best = agents[0]
    best_fitness = target_function(agents[0])

    for a in agents:
        if target_function(a) < best_fitness:
            best = a
            best_fitness = target_function(a)

    return target_function(best)


def run(params):

    cr_range, f_range, increment_step, repetitions, generation_size, \
    dimensions, iterations, b_lower, b_upper = params

    fitness = []

    cr_vals = [round(x, 6) for x in arange(cr_range[0], cr_range[1], increment_step).tolist()]
    f_vals = [round(x, 6) for x in arange(f_range[0], f_range[1], increment_step).tolist()]


    for cr in cr_vals:
        for f in f_vals:
            average_fitness = 0
            for r in range(repetitions):
                average_fitness += differential_evolution(cr, f, \
                                   generation_size, dimensions, iterations, \
                                   b_lower, b_upper)
            average_fitness /= repetitions
            fitness.append([cr, f, average_fitness])

    return fitness


def init():

    cpu_cores = 4
    cr_range = [0, 1]
    f_range = [0, 2]
    increment_step = 0.05
    repetitions = 10
    generation_size = 10
    dimensions = 2
    iterations = 20
    b_lower = -1
    b_upper = 1

    worker_tasks = []
    for core in range(cpu_cores):
        worker_tasks.append([
            [
                (core / cpu_cores) * (cr_range[1] - cr_range[0]),
                ((core + 1) / cpu_cores) * (cr_range[1] - cr_range[0]),
            ],
            [
                (core / cpu_cores) * (f_range[1] - f_range[0]),
                ((core + 1) / cpu_cores) * (f_range[1] - f_range[0]),
            ],
            increment_step,
            repetitions,
            generation_size,
            dimensions,
            iterations,
            b_lower,
            b_upper
        ])

    workers = Pool(cpu_cores)
    worker_results = workers.map(run, worker_tasks)

    results = []
    for core in worker_results:
        for result in core:
            results.append(result)

    with open('results.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        for line in range(len(results)):
            writer.writerow(results[line])

if __name__ == '__main__':
    init()
