from functools import wraps
from math import floor


def cached(f):
    cache = {}
    @wraps(f)
    def inner(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return inner


def read_data():
    with open('puzzle06.in', 'r') as f:
        return list(int(n) for n in next(f).strip().split(','))


def run(state, steps):
    for _ in range(steps):
        for idx in range(len(state)):
            if state[idx] == 0:
                state[idx] = 6
                state.append(8)
            else:
                state[idx] -= 1


def run2(state, steps):
    return sum(pop(steps, n) for n in state)


@cached
def pop(timespan, start):
    # print(f'*** pop({timespan}, {start}) ***')
    total = 1
    timespan -= start
    # print('timespan:', timespan, '|', 'total:', total)
    while timespan > 0:
        total += pop(timespan, 9)
        timespan -= 7
        # print('timespan:', timespan, '|', 'total:', total)
    # print('Returning:', total)
    return total


def part_1():
    state = read_data()
    run(state, 80)
    return len(state)


def part_2():
    state = read_data()
    return run2(state, 256)


def main():
    state = [int(n) for n in '3,4,3,1,2'.split(',')]
    run(state, 18)
    print(len(state), '(26)')
    run(state, 80 - 18)
    print(len(state), '(5934)')
    print()
    state = [int(n) for n in '3,4,3,1,2'.split(',')]
    print(run2(state, 18), '(26)')
    print(run2(state, 80), '(5934)')
    print(run2(state, 256), '(26984457539)')


if __name__ == '__main__':
    main()
