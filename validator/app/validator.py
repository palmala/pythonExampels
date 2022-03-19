import click
import os
import sys
import random
import json

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


@click.command(name='get_random_tests_per_tag')
@click.argument('path_to_tests', type=click.Path(exists=True), required=True)
@click.argument('number_of_tests', type=int, required=True)
@click.option('--untagged/--no-untagged', default=False)
@click.option('--js/--no-js', default=False)
def get_random_tests_per_tag(path_to_tests, number_of_tests, untagged, js):
    result = dict()
    tests_per_tags = tags.get_tests_per_tags(path_to_tests, "md")
    for tag in tests_per_tags:
        if not untagged and tag == "UNTAGGED":
            continue
        num = min([number_of_tests, len(tests_per_tags[tag])])
        result[tag] = random.sample(tests_per_tags[tag], k=num)
    _print_dict(js, result)

    sys.exit(0)


@click.command(name='get_tests_per_tags')
@click.argument('path_to_tests', type=click.Path(exists=True), required=True)
@click.option('--js/--no-js', default=False)
def get_tests_per_tags(path_to_tests, js):
    result = tags.get_tests_per_tags(path_to_tests, "md")
    _print_dict(js, result)
    sys.exit(0)


cli.add_command(get_tags)
cli.add_command(get_untagged)
cli.add_command(get_tests_for_tag)
cli.add_command(get_random_tests_per_tag)
cli.add_command(get_tests_per_tags)


def _print_dict(js, result):
    if js:
        print(json.dumps(result, indent=4))
    else:
        for k, v in result.items():
            print(k)
            for test_file in v:
                print(f"\t{test_file}")


if __name__ == "__main__":
    cli()
