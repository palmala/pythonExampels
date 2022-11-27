from random import randint
from collections import defaultdict


def generate_graph(num_nodes: int, num_edges: int):
    graph = dict()
    for i in range(num_nodes):
        graph[i] = list()

    edges = set()
    while len(edges) < num_edges:
        source = randint(0, num_nodes - 1)
        target = randint(0, num_nodes - 1)
        if source == target:
            continue
        if (source, target) not in edges:
            graph[source].append(target)
            edges.add((source, target))
    return graph


def bfs(graph: dict, start):
    distance = dict()
    parent = dict()
    distance[start] = 0
    parent[start] = -1

    processing = [start]
    while processing:
        current = processing.pop(0)
        for adj in graph[current]:
            if adj in parent:
                continue
            parent[adj] = current
            distance[adj] = distance[current] + 1
            processing.append(adj)

    bfs_tree = defaultdict(list)
    for k, v in parent.items():
        if v >= 0:
            bfs_tree[v].append(k)
    return bfs_tree, parent, distance
