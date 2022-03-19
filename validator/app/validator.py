import click
import os
import sys
from collections import defaultdict
import random

current_directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current_directory)
sys.path.append(parent)

from hr_test_lib import tags


@click.group()
def cli():
    pass


@click.command(name='get_tags')
@click.argument('path_to_tests', type=click.Path(exists=True), required=True)
def get_tags(path_to_tests):
    all_tags = tags.get_tags_from_tests(path_to_tests, "md")
    print(f"all tags: {all_tags}")
    for tag in all_tags:
        print(tag)
    sys.exit(len(all_tags) == 0)


@click.command(name='get_untagged')
@click.argument('path_to_tests', type=click.Path(exists=True), required=True)
def get_untagged(path_to_tests):
    untagged = tags.get_tests_per_tags(path_to_tests, "md")["UNTAGGED"]
    for testfile in untagged:
        print(testfile)
    sys.exit(len(untagged))


@click.command(name='get_tests_for_tag')
@click.argument('path_to_tests', type=click.Path(exists=True), required=True)
@click.argument('tag', type=str, required=True)
def get_tests_for_tag(path_to_tests, tag):
    tests_per_tags = tags.get_tests_per_tags(path_to_tests, "md")
    if tag in tests_per_tags:
        for testfile in tests_per_tags[tag]:
            print(testfile)
        sys.exit(0)
    else:
        raise AttributeError(f"No tests for tag {tag}")


cli.add_command(get_tags)
cli.add_command(get_untagged)
cli.add_command(get_tests_for_tag)

if __name__ == "__main__":
    cli()
