from collections import deque


def read_data():
    with open('puzzle15.in', 'r') as f:
        return[[int(c) for c in line.strip()] for line in f]


def expand_matrix(matrix):
    return [
        [
            ((value + vertical_repetition + horizontal_repetition - 1) % 9) + 1
            for horizontal_repetition in range(5)
            for value in row
        ]
        for vertical_repetition in range(5)
        for row in matrix
    ]


def build_graph(matrix):
    nrows, ncols = len(matrix), len(matrix[0])
    def neighbours(r, c):
        if r > 0:
            yield (r - 1, c)
        if r < nrows - 1:
            yield (r + 1, c)
        if c > 0:
            yield (r, c - 1)
        if c < ncols - 1:
            yield (r, c + 1)
    graph = {'nodes': {}, 'edges': {}}
    for r in range(nrows):
        for c in range(ncols):
            node = (r, c)
            graph['nodes'][node] = 1e6  # 'infinite' distance for Dijkstra
            graph['edges'][node] = {(nr, nc): matrix[nr][nc] for nr, nc in neighbours(r, c)}
    return graph


def build_graph2(matrix):
    from networkx import DiGraph
    nrows, ncols = len(matrix), len(matrix[0])
    def neighbours(r, c):
        if r > 0:
            yield (r - 1, c)
        if r < nrows - 1:
            yield (r + 1, c)
        if c > 0:
            yield (r, c - 1)
        if c < ncols - 1:
            yield (r, c + 1)
    graph = DiGraph()
    for r in range(nrows):
        for c in range(ncols):
            graph.add_edges_from(((r, c), (nr, nc), {'weight': matrix[nr][nc]})
                                 for nr, nc in neighbours(r, c))
    return graph


def min_risk(graph):
    start, end = (0, 0), max(graph['nodes'], key=sum)
    nodes, edges = graph['nodes'], graph['edges']
    nodes[start] = 0
    unvisited = set(nodes)
    while unvisited:
        node = min(unvisited, key=lambda n: nodes[n])
        current_risk = nodes[node]
        unvisited.remove(node)
        for n in set(edges[node]) & unvisited:
            if nodes[n] > (new_risk := current_risk + edges[node][n]):
                nodes[n] = new_risk
    return nodes[end]


def min_risk2(graph):
    from networkx import shortest_path_length
    start, end = (0, 0), max(graph.nodes, key=sum)
    return shortest_path_length(graph, start, end, weight='weight')


def part_1():
    graph = build_graph(read_data())
    return min_risk(graph)


def part_2():
    graph = build_graph2(expand_matrix(read_data()))
    return min_risk2(graph)


def main():
    matrix = [
        [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
        [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
        [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
        [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
        [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
        [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
        [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
        [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
        [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
        [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]
    ]
    graph = build_graph(matrix)
    print(min_risk(graph))
    graph = build_graph2(expand_matrix(matrix))
    print(min_risk2(graph))


if __name__ == '__main__':
    main()
