from collections import defaultdict


def reverse_edges(graph):
    result = defaultdict(list)
    for node in graph:
        if node not in result:
            result[node] = []
        for child in graph[node]:
            result[child].append(node)

    return result


def get_leveling(graph: {list}):
    result = dict()

    for node in graph:
        if not graph[node]:
            result[node] = 0
        else:
            result[node] = -1

    while any([result[x] == -1 for x in result]):
        for node in graph:
            if result[node] > -1:
                continue
            else:
                if all([result[x] > -1 for x in graph[node]]):
                    result[node] = max([result[x] for x in graph[node]]) + 1

    return result
