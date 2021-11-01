import multiprocessing
import time
import atexit
import random
import os

# def worker(*args):
#     print("Work, work...")
#     print(f'That is what I got: {args}')
#     time.sleep(random.randint(10, 20))


def calculate(value):
    print(f'Starting')
    return value * 10


def before_i_leave():
    print("Goodbye cruel world")

if __name__ == "__main__":
    atexit.register(before_i_leave)

    pool = multiprocessing.Pool(None)
    tasks = range(10)
    results = []
    r = pool.map_async(calculate, tasks, callback=results.append)
    r.wait() # Wait on the results
    print(results)

    # proc = multiprocessing.Process(target=worker, args=(12, 34, 56))
    # proc.start()
    # time.sleep(5)
    # proc.terminate()
