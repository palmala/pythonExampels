import math
import numpy
from matplotlib import pyplot


def zeta(s, iterations=50):
    if s <= 1:
        return None
    result = 1
    for i in range(2, iterations):
        next_iter = 1.0 / math.pow(i, s)
        result = result + next_iter
    return result


if __name__ == "__main__":
    xa = numpy.linspace(0, 4, 100)
    ya = list(map(zeta, xa))
    pyplot.plot(xa, ya)
    pyplot.show()
