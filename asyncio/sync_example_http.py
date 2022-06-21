import time
import requests

SOURCE = "http://127.0.0.1:5000/"


def gather_data():
    response = requests.get(SOURCE)
    return response.json()


def generate_data(p):
    first_data = gather_data()["value"]
    second_data = gather_data()["value"]
    return [p, first_data, second_data, f"{p}{first_data}{second_data}"]


def main(number):
    start = time.perf_counter()
    projects = [f"project{i}" for i in range(number)]
    for project in projects:
        print(generate_data(project))
    print(f"Execution took {time.perf_counter() - start} seconds")


if __name__ == "__main__":
    main(10)
