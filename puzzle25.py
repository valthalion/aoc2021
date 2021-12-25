def read_data(test=False):
    filename = 'puzzle25-test.in' if test else 'puzzle25.in'
    east, south = set(), set()
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            for c, cucumber in enumerate(line.strip()):
                if cucumber == '>':
                    east.add((r, c))
                elif cucumber == 'v':
                    south.add((r, c))
    return c + 1, r + 1, east, south


def step(width, height, east, south):
    east_origins, east_dests = set(), set()
    for r, c in east:
        move = (r, (c + 1) % width)
        if move not in east and move not in south:
            east_origins.add((r, c))
            east_dests.add(move)
    east -= east_origins
    east |= east_dests

    south_origins, south_dests = set(), set()
    for r, c in south:
        move = ((r + 1) % height, c)
        if move not in east and move not in south:
            south_origins.add((r, c))
            south_dests.add(move)
    south -= south_origins
    south |= south_dests

    return True if east_origins or south_origins else False


def time_to_stop(width, height, east, south):
    steps = 0
    while step(width, height, east, south):
        steps += 1
    return steps + 1  # question is first step with no moves, not last with moves


def part_1():
    return time_to_stop(*read_data())


def part_2():
    pass


def main():
    print(time_to_stop(*read_data(test=True)))


if __name__ == '__main__':
    main()
