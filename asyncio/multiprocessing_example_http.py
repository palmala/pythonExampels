import time
import requests
import multiprocessing

SOURCE = "http://127.0.0.1:5000/"


def gather_data():
    response = requests.get(SOURCE)
    return response.json()


def generate_data(p):
    first_data = gather_data()["value"]
    second_data = gather_data()["value"]
    return [p, first_data, second_data, f"{p}{first_data}{second_data}"]


def process_projects(number):
    projects = [f"project{i}" for i in range(number)]
    results = []
    tasks = []
    pool = multiprocessing.Pool(8)
    for project in projects:
        t = pool.apply_async(generate_data, (project,), callback=results.append)
        tasks.append(t)
    for t in tasks:
        try:
            t.wait()
        except Exception as err:
            print(f"[ERROR]: Exception during task exec: {err}")

    for result in results:
        print(result)


def main():
    start = time.perf_counter()
    process_projects(10)
    print(f"Execution took {time.perf_counter() - start} seconds")


if __name__ == "__main__":
    main()
