#! /usr/bin/python3

from csv import reader
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D, get_test_data
from matplotlib import cm
import numpy as np
import csv

X = np.arange(0, 1, 0.01)
Y = np.arange(0, 2, 0.01)
Z = np.zeros(shape=(20000))

z_counter = 0
with open('results.csv', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar=';', quoting=csv.QUOTE_MINIMAL)
    for row in spamreader:
        Z[z_counter] = row[2]
        z_counter += 1

X, Y = np.meshgrid(X, Y)
Z = Z.reshape(200, 100)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

plt.xlabel('CR')
plt.ylabel('F')

plt.show()