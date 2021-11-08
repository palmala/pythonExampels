import math
import multiprocessing
import time
from itertools import repeat
import sympy.ntheory

from sympy import ntheory

numbers = [2, 3, 7, 43, 13, 53, 5, 6221671, 38709183810571, 139, 2801, 11, 17, 5471, 52662739, 23003]
# numbers = [2, 3, 7, 43, 13, 53, 5, 6221671, 38709183810571, 139, 2801, 11, 17, 5471]
start_from = 11060000000


def calculate(num, i):
    if num % i == 0:
        return i
    else:
        return None


def sequential():
    print(f'Sequential test started')
    new_num = math.prod(numbers) + 1
    print(f'Looking for smallest prime divisor for {new_num}')
    limit = int(math.sqrt(new_num))
    next_prime = None
    print(f'Starting calculation')
    for i in sympy.ntheory.generate.primerange(limit):
        if new_num % i == 0:
            next_prime = i
            break
    print(f'Prime found {next_prime}')
    return next_prime


def calculate_chunks(*arguments):
    result = None
    (lower_bound, chunk_size, number) = arguments[0]
    for p in ntheory.primerange(lower_bound, lower_bound + chunk_size):
        if number % p == 0:
            result = p
            break
    print(f'Finished check for range ({lower_bound}, {lower_bound + chunk_size})')
    return result


def distributed():
    new_num = math.prod(numbers) + 1
    print(f'Looking for smallest prime divisor for {new_num}')
    limit = int(math.sqrt(new_num))
    chunk_size = 2 * (10 ** 7)
    parameters = zip(range(start_from, limit + 1, chunk_size), repeat(chunk_size), repeat(new_num))

    pool = multiprocessing.Pool(None)
    result = pool.imap(calculate_chunks, parameters)
    next_prime = []
    for r in result:
        if r:
            next_prime.append(r)
            break
    pool.terminate()
    pool.join()
    for r in result:
        print(r)
    return min(next_prime)


if __name__ == "__main__":
    print(f'Calculations started')
    start = time.time()
    # res = sequential()
    res = distributed()
    end = time.time()
    print(f'Time taken {end - start}')
