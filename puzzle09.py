from collections import defaultdict
from math import prod


def read_data():
    with open('puzzle09.in', 'r') as f:
        return [[int(n) for n in line.strip()] for line in f]


def neighbours_fun(map):
    R, C = len(map), len(map[0])

    def neighbours(r, c):
        if r > 0:
            yield r -1, c
        if r < R - 1:
            yield r + 1, c
        if c > 0:
            yield r, c - 1
        if c < C - 1:
            yield r, c + 1

    return neighbours


def find_low_points(map):
    neighbours = neighbours_fun(map)
    for r, row in enumerate(map):
        for c, value in enumerate(row):
            if all(value < map[nr][nc] for nr, nc in neighbours(r, c)):
                yield r, c


def build_graph(map):
    neighbours = neighbours_fun(map)
    graph = defaultdict(set)
    for r, row in enumerate(map):
        for c, value in enumerate(row):
            if value == 9:
                continue
            for nr, nc in neighbours(r, c):
                if map[nr][nc] != 9:
                    graph[(r, c)].add((nr, nc))
    return graph


def connected_components(graph):
    nodes = set(graph)
    while nodes:
        component = set()
        queue = set()
        queue.add(nodes.pop())
        while queue:
            node = queue.pop()
            component.add(node)
            neighbours = graph[node] & nodes
            nodes -= neighbours
            queue |= neighbours
        yield component


def n_largest(graph, n):
    return sorted([len(c) for c in connected_components(graph)], reverse=True)[:n]


def part_1():
    map = read_data()
    return sum(1 + map[r][c] for r, c in find_low_points(map))


def part_2():
    map = read_data()
    graph = build_graph(map)
    return(prod(n_largest(graph, 3)))


def main():
    map = [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
           [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
           [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
           [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
           [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]
    low_points = find_low_points(map)
    print([map[r][c] for r, c in low_points])
    print('---')
    graph = build_graph(map)
    print(prod(n_largest(graph, 3)))


if __name__ == '__main__':
    main()
