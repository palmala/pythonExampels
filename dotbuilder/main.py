from dotbuilder import *
from dummy_projects_provider import DummyProjectsProvider

import os
import shutil
import logging

OUTPUT = "build"
FILENAMES = "{basedir}/{filename}.dot"
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    shutil.rmtree(OUTPUT, ignore_errors=True)
    os.makedirs(OUTPUT)

    logging.info("Getting projects")
    projects = DummyProjectsProvider().get_projects()

    logging.info("Creating base graph")
    subject = dot_builder(projects, "base_projects")
    write_to_file(subject, FILENAMES.format(basedir=OUTPUT, filename="base_projects"))

    instability = calculate_instability(subject)
    calculate_violations(subject, instability)
    write_to_file(subject, FILENAMES.format(basedir=OUTPUT, filename="base_projects_violations"))

    detect_all_cycles(subject)

    categories = classify_nodes_per_instability(subject, instability)

    dependants = get_all_dependants(mygraph=subject, node_name="A")
    write_to_file(dependants, FILENAMES.format(basedir=OUTPUT, filename="dependants_A"))
