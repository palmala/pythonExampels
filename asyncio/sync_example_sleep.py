import time
import random


def gather_data():
    time.sleep(1)
    return random.randint(1, 10)


def generate_data(p):
    first_data = gather_data()
    second_data = gather_data()
    return [p, first_data, second_data, f"{p}{first_data}{second_data}"]


def main(number):
    start = time.perf_counter()
    projects = [f"project{i}" for i in range(number)]
    for project in projects:
        print(generate_data(project))
    print(f"Execution took {time.perf_counter() - start} seconds")


if __name__ == "__main__":
    main(10)
