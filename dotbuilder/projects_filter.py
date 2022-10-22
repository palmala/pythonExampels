from collections import defaultdict


def restrict_projects(projects, restrictions):
    restricted = defaultdict(list)
    for project in projects:
        if project not in restrictions:
            continue
        for dependency in projects[project]:
            if dependency in restrictions:
                restricted[project].append(dependency)

    return restricted
