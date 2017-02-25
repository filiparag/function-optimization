#! /usr/bin/python3

from csv import reader
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import csv

X = np.arange(0, 1, 0.02)
Y = np.arange(0, 2, 0.02)
Z = np.zeros(shape=(5000))

z_counter = 0
with open('results.csv', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar=';', quoting=csv.QUOTE_MINIMAL)
    for row in spamreader:
        Z[z_counter] = row[2]
        z_counter += 1

X, Y = np.meshgrid(X, Y)
Z = Z.reshape(100, 50)

plt.pcolormesh(X, Y, Z)

cb = plt.colorbar()
cb.ax.get_yaxis().labelpad = 15
cb.ax.set_ylabel('Fitness', rotation=90)

plt.xlabel('Crossover Probability')
plt.ylabel('Differential Weight')

plt.show()