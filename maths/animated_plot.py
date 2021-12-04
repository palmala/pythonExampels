from matplotlib.animation import FuncAnimation
import matplotlib
from matplotlib import pyplot

import numpy
import math


def f(x):
    return math.pow(x, 2)


def animate(i):
    x = numpy.linspace(0, 1, 100)
    y = f(x, 0.5)


if __name__ == "__main__":
    print("Hi")
    fig = pyplot.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    f_d = ax.plot([], [])
