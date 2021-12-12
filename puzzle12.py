from collections import defaultdict


def read_data():
    with open('puzzle12.in', 'r') as f:
        for line in f:
            yield line.strip().split('-')


def build_graph(edges):
    graph = defaultdict(set)
    small_caves = set()
    large_caves = set()
    for edge in edges:
        orig, dest = edge
        graph[orig].add(dest)
        graph[dest].add(orig)
    for node in graph:
        (small_caves if node.lower() == node else large_caves).add(node)
    return graph, small_caves, large_caves


def find_paths(graph, small_caves, large_caves, current_node='start', visited=None, small_return = False):
    if current_node == 'end':
        return 1
    if visited is None:
        visited = set()
    if current_node in small_caves:
        visited.add(current_node)
    total_paths = 0
    neighbours = graph[current_node]
    if small_return:
        neighbours = neighbours - {'start'}
    else:
        neighbours = neighbours - visited
    for neighbour in neighbours:
        next_small_return = small_return and neighbour not in visited
        total_paths += find_paths(graph, small_caves, large_caves,
            current_node=neighbour, visited=set(visited), small_return=next_small_return)
    return total_paths


def part_1():
    graph, small_caves, large_caves = build_graph(read_data())
    return find_paths(graph, small_caves, large_caves)


def part_2():
    graph, small_caves, large_caves = build_graph(read_data())
    return find_paths(graph, small_caves, large_caves, small_return=True)


def main():
    map1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    map2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
    map3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
    print(find_paths(*build_graph(line.strip().split('-') for line in map1.split('\n'))), 10)
    print(find_paths(*build_graph(line.strip().split('-') for line in map2.split('\n'))), 19)
    print(find_paths(*build_graph(line.strip().split('-') for line in map3.split('\n'))), 226)
    print('---')
    print(find_paths(*build_graph(line.strip().split('-') for line in map1.split('\n')), small_return=True), 36)
    print(find_paths(*build_graph(line.strip().split('-') for line in map2.split('\n')), small_return=True), 103)
    print(find_paths(*build_graph(line.strip().split('-') for line in map3.split('\n')), small_return=True), 3509)


if __name__ == '__main__':
    main()
