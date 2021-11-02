import atexit
import multiprocessing
import os
import platform
import random
import threading
import time


# def worker(*args):
#     print("Work, work...")
#     print(f'That is what I got: {args}')
#     time.sleep(random.randint(10, 20))


def calculate(value):
    num = random.randint(2, 10)
    num = 5
    print(f'{multiprocessing.current_process()} Calculating {value} for {num} seconds')
    time.sleep(num)
    print(f'{multiprocessing.current_process()} Ending calculation for {value}')
    return value * 10


def before_i_leave(result):
    print("Goodbye cruel world")
    print(result)


if __name__ == "__main__":
    #    atexit.register(before_i_leave, results)
    start = time.time()
    results = []
    tasks = []
    pool = multiprocessing.Pool(2)
    for task in range(100):
        r = pool.apply_async(calculate, (task, ), callback=results.append)
        results.append(r)
    for r in results:
        r.wait()
    print(results)
    end = time.time()
    print(f'Calculations took {end - start} seconds')

    # proc = multiprocessing.Process(target=worker, args=(12, 34, 56))
    # proc.start()
    # time.sleep(5)
    # proc.terminate()
