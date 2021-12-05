from collections import defaultdict
from itertools import repeat


def parse_line(line):
    return tuple(tuple(int(x) for x in p.split(',')) for p in line.split(' -> '))


def read_data(only_ortho=True):
    with open('puzzle05.in', 'r') as f:
        for line in f:
            l = ((x1, y1), (x2, y2)) = parse_line(line.strip())
            if not only_ortho or x1 == x2 or y1 == y2:
                yield l


def run_line(line):
    ((x1, y1), (x2, y2)) = line
    if x1 == x2:
        y_low, y_high = min(y1, y2), max(y1, y2) + 1
        yield from zip(repeat(x1), range(y_low, y_high))
    elif y1 == y2:
        x_low, x_high = min(x1, x2), max(x1, x2) + 1
        yield from zip(range(x_low, x_high), repeat(y1))
    else:
        delta_x = 1 if x2 > x1 else -1
        x_range = range(x1, x2 + delta_x, delta_x)
        delta_y = 1 if y2 > y1 else -1
        y_range = range(y1, y2 + delta_y, delta_y)
        yield from zip(x_range, y_range)


def build_map(lines):
    map = defaultdict(int)
    for line in lines:
        for point in run_line(line):
            map[point] += 1
    return map


def part_1():
    lines = read_data()
    map = build_map(lines)
    return sum(1 for count in map.values() if count > 1)


def part_2():
    lines = read_data(only_ortho=False)
    map = build_map(lines)
    return sum(1 for count in map.values() if count > 1)


def main():
    lines = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
    parsed_lines = [parse_line(line) for line in lines.split('\n')]
    ortho_lines = [((x1, y1), (x2, y2)) for ((x1, y1), (x2, y2)) in parsed_lines
                   if x1 == x2 or y1 == y2]
    map = build_map(ortho_lines)
    print(sum(1 for count in map.values() if count > 1))
    map = build_map(parsed_lines)
    print(sum(1 for count in map.values() if count > 1))
    


if __name__ == '__main__':
    main()
