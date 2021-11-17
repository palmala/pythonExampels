import math
import numpy
from matplotlib import pyplot


def zeta(s, iterations=50):
    if s <= 1:
        raise AttributeError('ERROR: zeta is not defined for arguments <= 1!')

    # a compact way is return sum(list(map(lambda i: (math.pow(1, i + 1)) / math.pow(i, s), range(2, iterations))))
    # but I leave this here for readability purposes

    result = 1
    for i in range(2, iterations):
        next_iter = 1.0 / math.pow(i, s)
        result = result + next_iter
    return result


def eta(s, iterations=50):
    if s < 0 or s >= 1:
        return None
    result = 1
    for i in range(2, iterations):
        next_iter = (math.pow(1, i + 1)) / math.pow(i, s)
        result = result + next_iter

    return result


def combined(s, iterations=50):
    if s < 0:
        return None
    elif s < 1:
        return eta(s, iterations) / (1.0 - (1.0 / math.pow(2, s - 1)))
    elif s == 1:
        return None
    else:
        return zeta(s, iterations)


if __name__ == "__main__":
    xa = numpy.linspace(1, 5, 100)
    pyplot.subplot(121)
    pyplot.title("Zeta function for 1 < s < 5")
    pyplot.ylabel("zeta(s)")
    pyplot.xlabel("s")
    ya = list(map(combined, xa))
    pyplot.plot(xa, ya)

    pyplot.subplot(122)
    pyplot.title("Zeta function for 0 < s < 1")
    pyplot.ylabel("zeta(s)")
    pyplot.xlabel("s")
    xa = numpy.linspace(0, 1, 100)
    ya = list(map(combined, xa))
    pyplot.plot(xa, ya)
    pyplot.show()
