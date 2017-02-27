from math import sqrt, exp, cos, sin, pi

def target_function(params):

    # Ackley
    # result = -20 * exp(-0.2 * sqrt(0.5 * (params[0] ** 2 + params[1] ** 2))) - \
    #          exp(0.5 * (cos(6.2 * params[0]) + cos(6.2 * params[1]))) + 2.71 + 20

    # Beale
    # result = (1.5 - params[0] + params[0] * params[1]) ** 2 + (2.25 - params[0] \
    #          + params[0] * (params[1] ** 2)) ** 2 + \
    #          (2.625 - params[0] + params[0] * (params[1] ** 3)) ** 2

    # Bukin02    [-15, 5] [-3, 3]
    # result = 100 * (params[1] - 0.01 * params[0] ** 2 +1) + 0.01(params[0] + 10) ** 2

    # AMGM [0,10]
    # result = 0.5 * ((params[0] + params[1]) - sqrt(params[0] * params[1])) ** 2

    # Sodp [-1, 1]
    # result =  abs(params[0] * 2) + abs(params[1] * 3)

    # Treecani [-5, 5]
    # result = params[0] ** 4 +   4 * params[0] ** 3 + 4 * params[0] ** 2 + params[1] ** 2

    # Trigonometric2 [-500, 500]
    # result = (1 + 8 * (sin(7 * (params[0] - 0.9) ** 2)) ** 2 + 6 * (sin(14 * (params[0] \
    #          - 0.9) ** 2)) ** 2 + (params[0] - 0.9) ** 2) + (1 + 8 * (sin(7 * (params[1] \
    #          - 0.9) ** 2)) ** 2 + 6 * (sin(14 * (params[1] - 0.9) ** 2)) ** 2 + \
    #          (params[1] - 0.9) ** 2)


    # Cosine Mixture  [-1, 1]
    # result = -0.1 * (cos(5 * pi * params[0]) + cos(5 * pi * params[1])) - (params[0] \
    #          ** 2 + params[1] ** 2)

    # Rosenbrock
    result = 0
    try:
        for i in range(len(params) - 1):
            result += 100 * (params[i + 1] - params[i] ** 2) ** 2 + (params[i] - 1) ** 2

    except OverflowError:
        result = float('inf')

    return result
