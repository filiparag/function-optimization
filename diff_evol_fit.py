#! /usr/bin/python3

from random import random, randint
# from multiprocessing import Pool
from numpy import arange
import csv
from target_function import target_function
from scoop import futures


def differential_evolution(params):

    cr, f, b_lo, b_up, np, dim, it_s, it_t = params

    agents = [[(random() * (b_up - b_lo)) for x in range(dim)] for a in range(np)]

    results = []
    best, best_fitness = None, None

    for i in range(it_t + 1):
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

        if i % it_s == 0:

            if best is None:
                best = agents[0]
                best_fitness = target_function(agents[0])

            for a in agents:
                if target_function(a) < best_fitness:
                    best = a
                    best_fitness = target_function(a)

            results.append(best)

    return results


def init():

    cpu_cores = 4
    cr = 0.8803
    f = 0.4717
    b_lower = -2
    b_upper = 2
    generation_size = 200
    dimensions = 20
    iteration_step = 5
    iteration_target = 1000
    repetitions = 2

    worker_tasks = [[
        cr,
        f,
        b_lower,
        b_upper,
        generation_size,
        dimensions,
        iteration_step,
        iteration_target,
    ]] * repetitions

    # single computer
    # workers = Pool(cpu_cores)
    # worker_results = workers.map(differential_evolution, worker_tasks)

    # cluster computer
    worker_results = list(futures.map(differential_evolution, worker_tasks))

    results = []
    for i in range(int(iteration_target / iteration_step) + 1):
        iteration_result = [0] * dimensions

        for thread in worker_results:
            iteration_result = [sum(x) for x in zip(iteration_result, thread[i])]

        iteration_result = [x / repetitions for x in iteration_result]
        results.append(iteration_result)

    print(results[-1])

    fitness = (target_function(r) for r in results)

    with open('results.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        for line in fitness:
            writer.writerow([line])

if __name__ == '__main__':
    init()
