#! /usr/bin/python3

from csv import reader
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import csv
from math import log

X = np.arange(0, 10005, 5)
Y = np.zeros(shape=(2001))

y_counter = 0
with open('results.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar=';', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        Y[y_counter] = row[0]
        y_counter += 1

Y = Y.tolist()
# Y = [log(i) if i > 0 else 0 for i in Y]

plt.plot(X, Y)

plt.xlabel('Number of iterations')
plt.ylabel('Fitness [log]')

plt.show()