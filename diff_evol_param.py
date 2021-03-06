#! /usr/bin/python3

from random import random, randint
from multiprocessing import Pool
from numpy import arange
import csv
from target_function import target_function
# from scoop import futures


def differential_evolution(cr, f, np, dim, it, b_lo, b_up):

    agents = [[(random() * (b_up - b_lo)) for x in range(dim)] for a in range(np)]

    for i in range(it):
        for x in range(np):

            a, b, c = randint(0, np - 1), randint(0, np - 1), randint(0, np - 1)
            while a == b or b == c or c == a or a == x or b == x or c == x:
                a, b, c = randint(0, np - 1), randint(0, np - 1), randint(0, np - 1)

            R = randint(0, dim)
            y = [None] * dim

            for j in range(dim):
                ri = random()
                if ri < cr or j == R:
                    y[j] = agents[a][j] + f * (agents[b][j] - agents[c][j])
                else:
                    y[j] = agents[x][j]

            if target_function(y) < target_function(agents[x]):
                agents[x] = y

    best = agents[0]
    best_fitness = target_function(agents[0])

    for a in agents:
        if target_function(a) < best_fitness:
            best = a
            best_fitness = target_function(a)

    return best


def run(params):

    cr_range, f_range, increment_step, repetitions, generation_size, \
    dimensions, iterations, b_lower, b_upper = params

    fitness = []

    cr_vals = [round(x, 6) for x in arange(cr_range[0], cr_range[1], increment_step).tolist()]
    f_vals = [round(x, 6) for x in arange(f_range[0], f_range[1], increment_step).tolist()]

    for f in f_vals:
        for cr in cr_vals:

            average_fitness = 0
            average_position = [0] * dimensions

            for r in range(repetitions):
                position = differential_evolution(cr, f, \
                           generation_size, dimensions, iterations, \
                           b_lower, b_upper)
                average_fitness += target_function(position)
                average_position = [sum(x) for x in zip(average_position, position)]

            average_fitness /= repetitions
            average_position = [x / repetitions for x in average_position]
            fitness.append([cr, f, average_fitness])

    return fitness


def init():

    cpu_cores = 4
    cr_range = [0, 1]
    f_range = [0, 2]
    increment_step = 0.01
    repetitions = 1
    generation_size = 40
    dimensions = 4
    iterations = 100
    b_lower = -2
    b_upper = 2

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
        if r[2] < best_fitness[2]:
            best_fitness = r

    print(best_fitness)

    with open('results.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        for line in results:
            writer.writerow([line[2]])


if __name__ == '__main__':
    init()
