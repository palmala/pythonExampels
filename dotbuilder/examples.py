from dotbuilder import *

import os
import shutil
import logging

OUTPUT = "examples"
FILENAMES = "{basedir}/{filename}.dot"
logging.basicConfig(level=logging.INFO)


def process_example(projects, name):
    subject = dot_builder(projects, name)
    instability = calculate_instability(subject)
    calculate_violations(subject, instability)
    average_i = float(sum(list(instability.values()))) / len(subject.get_edges())
    graph_i = average_i * len(subject.get_edge_list())
    print(f"Name: {name}, Average I: {average_i}, Graph level I: {graph_i}")
    write_to_file(subject, FILENAMES.format(basedir=OUTPUT, filename=name))
    return subject


def main():
    shutil.rmtree(OUTPUT, ignore_errors=True)
    os.makedirs(OUTPUT)

    projects = {
        'A': [],
        'B': ['A'],
        'C': ['A'],
        'D': ['A']
    }
    process_example(projects, "maxI")

    projects = {
        'A': [],
        'B': ['A', 'C'],
        'C': ['A'],
        'D': ['A']
    }
    process_example(projects, "maxI2")

    projects = {
        'A': [],
        'B': ['A', 'C'],
        'C': ['A', 'D'],
        'D': ['A']
    }
    process_example(projects, "maxI3")

    projects = {
        'A': ['B', 'C', 'D'],
        'B': [],
        'C': [],
        'D': []
    }
    process_example(projects, "minI")

    projects = {
        'A': ['B', 'C', 'D'],
        'B': ['C'],
        'C': [],
        'D': []
    }
    process_example(projects, "minI2")

    projects = {
        'A': ['B', 'C', 'D'],
        'B': ['C'],
        'C': ['D'],
        'D': []
    }
    process_example(projects, "minI3")


if __name__ == "__main__":
    main()
