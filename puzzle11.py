def read_data():
    with open('puzzle11.in', 'r') as f:
        return [[int(c) for c in line.strip()] for line in f]


def build_graph(matrix):
    R, C = len(matrix), len(matrix[0])
    def neighbours(r, c):
        rc_reighbours = set((nr, nc)
                            for nr in range(max(r - 1, 0), min(r + 2, R))
                            for nc in range(max(c - 1, 0), min(c + 2, C))
                            if (nr, nc) != (r, c)
                            )
        return rc_reighbours
    graph = {}
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            graph[(r, c)] = {'energy': value, 'neighbours': neighbours(r, c)}
    return graph


def step(graph):
    flashes = set()
    queue = list(graph)
    while queue:
        octopus = queue.pop()
        if octopus in flashes:
            continue
        if graph[octopus]['energy'] == 9:
            flashes.add(octopus)
            queue.extend(graph[octopus]['neighbours'] - flashes)
            graph[octopus]['energy'] = 0
        else:
            graph[octopus]['energy'] += 1
    return len(flashes)


def play(graph, n_steps=None):
    if n_steps is not None:
        return sum(step(graph) for _ in range(n_steps))
    n_steps = 0
    while True:
        n_steps += 1
        n_flashes = step(graph)
        if n_flashes == len(graph):
            return n_steps


def part_1():
    graph = build_graph(read_data())
    return play(graph, 100)


def part_2():
    graph = build_graph(read_data())
    return play(graph)


def main():
    matrix = [[5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
              [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
              [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
              [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
              [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
              [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
              [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
              [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
              [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
              [5, 2, 8, 3, 7, 5, 1, 5, 2, 6]]
    print(play(build_graph(matrix), 100))
    print(play(build_graph(matrix)))


if __name__ == '__main__':
    main()
