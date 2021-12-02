from collections import defaultdict


def read_data():
    with open('puzzle02.in', 'r') as f:
        for line in f:
            direction, arg = line.strip().split()
            yield direction, int(arg)


def run(commands):
    accumulator = defaultdict(int)
    for direction, arg in commands:
        accumulator[direction] += arg
    return accumulator['forward'], accumulator['down'] - accumulator['up']


def run2(commands):
    advance, depth, aim = 0, 0, 0
    for command, arg in commands:
        if command == 'up':
            aim -= arg
        elif command == 'down':
            aim += arg
        elif command == 'forward':
            advance += arg
            depth += aim * arg
        else:
            raise RuntimeError('Unknown command:', command)
    return advance, depth


def part_1():
    advance, depth = run(read_data())
    return advance * depth


def part_2():
    advance, depth = run2(read_data())
    return advance * depth


def main():
    commands = [('forward', 5), ('down', 5), ('forward', 8), ('up', 3), ('down', 8), ('forward', 2)]
    advance, depth = run(commands)
    print('Test part 1:', advance * depth)
    advance, depth = run2(commands)
    print('Test part 2:', advance * depth)


if __name__ == '__main__':
    main()
