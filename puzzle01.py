def read_data():
    with open('puzzle01.in', 'r') as f:
        return [int(line.strip()) for line in f]


def sliding_sum(numbers, window):
    N = len(numbers)
    return [sum(numbers[idx : idx+window]) for idx in range(N - window + 1)]


def increasing(numbers):
    diffs = (succ - pred for pred, succ in zip(numbers, numbers[1:]))
    return sum(1 for diff in diffs if diff > 0)


def part_1():
    return increasing(read_data())


def part_2():
    return increasing(sliding_sum(read_data(), window=3))


def main():
    numbers = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    n = increasing(numbers)
    print('Increasing measurements:', n)
    n = increasing(sliding_sum(numbers, window=3))
    print('Increasing measurements:', n)


if __name__ == '__main__':
    main()
