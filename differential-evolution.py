#! /usr/bin/python3

import random
import math
import matplotlib.pyplot as plt

def target_function(params):

    result = 0

    # Ackley
    result = -20 * math.exp(-0.2 * math.sqrt(0.5 * (params[0] ** 2 + params[1] ** 2))) - \
            math.exp(0.5 * (math.cos(6.2 * params[0]) + math.cos(6.2 * params[1]))) + 2.71 + 20

    # Beale
    # result = (1.5 - params[0] + params[0] * params[1]) ** 2 + (2.25 - params[0] + params[0] * (params[1] ** 2)) ** 2 + \
    #         (2.625 - params[0] + params[0] * (params[1] ** 3)) ** 2

    # Rosenbrock
    # for i in range(len(params) - 1):
    #     result += 100 * (params[i + 1] - params[i] ** 2) ** 2 + (params[i] - 1) ** 2

    return result

def diff_evol(cr, f, np, dim, it, b_lo=-1, b_up=1):

    agents = []

    for x in range(np):
        a = []
        for y in range(dim):
            a.append(random.random() * (b_up - b_lo))
        agents.append(a)

    for i in range(it):

        for x in range(np):

            a, b, c = random.randint(0, np - 1), random.randint(0, np - 1), random.randint(0, np - 1)
            while a == b or b == c or c == a or a == x or b == x or c == x:
                a, b, c = random.randint(0, np - 1), random.randint(0, np - 1), random.randint(0, np - 1)

            R = random.randint(0, dim)

            y = [None] * (dim)

            for i in range(dim):

                ri = random.random()

                if ri < cr or i == R:
                    y[i] = agents[a][i] + f * (agents[b][i] - agents[c][i])

                else:
                    y[i] = agents[x][i]

            if target_function(y) < target_function(agents[x]):
                agents[x] = y

            # plt.scatter(agents[x][0], agents[x][1])

        # plt.xlim(b_lo, b_up)
        # plt.ylim(b_lo, b_up)
        # plt.show()

    best = agents[0]

    for a in agents:

        if target_function(a) < target_function(best):

            best = a

    return best

if __name__ == '__main__':

    best = None

    for cr in range(0, 110, 1):
        for f in range(0, 210, 1):
            pom = diff_evol(cr / 100, f / 100, 200, 2, 1000, -10, 10) #cr, f, np, dim, it, b_lo=-1, b_up=1
            if best == None or target_function(pom) < best[2]:
                best = [cr / 100, f / 100, target_function(pom), pom]

    print(best)
            