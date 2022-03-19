import os
import re
from collections import defaultdict

TAGS_RE = "(?i)tags:(.*)"


def get_files_from_path(path, extension=""):
    files = []
    for file in os.scandir(path):
        if file.is_file() and file.name.endswith(extension):
            files.append(file.name)
    return files


def get_tests_per_tags(path, extension=""):
    files = get_files_from_path(path, extension)
    tags = defaultdict(list)
    for file in files:
        current_test_file = os.path.join(path, file)
        with open(current_test_file, 'r') as current_test:
            lines = current_test.readlines()
            tags_lines = [line.replace(" ", "") for line in lines if re.match(TAGS_RE, line.replace(" ", ""))]
            if tags_lines:
                match = re.search(TAGS_RE, tags_lines[0])
                for tag in match.group(1).split(","):
                    tags[tag].append(current_test_file)
            else:
                tags["UNTAGGED"].append(current_test_file)
    return tags


def get_tags_from_tests(path, extension=""):
    files_per_tags = get_tests_per_tags(path, "md")
    return [tag for tag in files_per_tags.keys() if tag != "UNTAGGED"]
