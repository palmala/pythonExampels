import multiprocessing
import random
import time
from sympy import ntheory


def calculate(*args):
    num = random.randint(2, 10)
    numbers = list(args)
    print(f'{multiprocessing.current_process()} Calculating {numbers} for {num} seconds')
    time.sleep(num)
    print(f'{multiprocessing.current_process()} Ending calculation for {numbers}')
    return sum(numbers)


# num = 26889089129721955323215873
if __name__ == "__main__":
    start = time.time()
    results = []
    tasks = []
    pool = multiprocessing.Pool(2)
    res = pool.imap(calculate, range(10), chunksize=2)
    for r in res:
        results.append(r)
        print(f'Updated results: {results}')
    end = time.time()
    print(f'Calculations took {end - start} seconds')
