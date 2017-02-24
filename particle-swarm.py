import random

def target_function(params):

    result = 0

    for p in params:

        result += pow(p, 2)

    return result

swarm_best = None

class Particle:

    def __init__(self, dim, b_up, b_lo):

        global swarm_best

        self.position = []

        for i in range(0, dim):
            self.position.append(random.random() * (b_up - b_lo))

        self.velocity = []

        for i in range(0, dim):
            self.velocity.append(random.random() * (-abs(b_up - b_lo) + abs(b_up - b_lo)))

        self.best = self.position

        if swarm_best == None:
            swarm_best = self.best

        elif target_function(self.best) < target_function(swarm_best):
            self.best = swarm_best


def pso(it, np, dim, b_up, b_lo, omega, phi_p, phi_g):

    global swarm_best

    swarm = []

    for i in range(np):
        swarm.append(Particle(dim, b_lo, b_up))

    for i in range(it):

        for particle in swarm:

            for d in range(dim):

                rp, rg = random.random(), random.random()

                particle.velocity[d] = omega * particle.velocity[d] + phi_p * rp * (particle.best[d] - particle.position[d]) + phi_g * rg * (swarm_best[d] - particle.position[d])

                particle.position[d] += particle.velocity[d]

            if target_function(particle.position) < target_function(particle.best):

                particle.best = particle.position

                if target_function(particle.best) < target_function(swarm_best):

                    swarm_best = particle.best

    return target_function(swarm_best), swarm_best

if __name__ == '__main__':

    print(pso(20, 10, 2, 2, -2, 1, 1, 1)) # it, np, dim, b_up, b_lo, omega, phi_p, phi_g