def read_data():
    with open('puzzle03.in', 'r') as f:
        return [[int(c) for c in line.strip()] for line in f]


def transpose(matrix):
    return list(zip(*matrix))


def calc_gamma(matrix):
    counts = [sum(row) for row in transpose(matrix)]
    threshold = len(matrix) // 2
    return [1 if count > threshold else 0 for count in counts]


def calc_epsilon(gamma):
    return [1 - x for x in gamma]


def decimal(binary):
    total = 0
    for x in binary:
        total *= 2
        total += x
    return total


def power(matrix):
    gamma = calc_gamma(matrix)
    epsilon = calc_epsilon(gamma)
    return decimal(gamma) * decimal(epsilon)


def oxygen_generator_rating(matrix):
    remaining = tuple(tuple(row) for row in matrix)
    current_col_idx = 0
    while len(remaining) > 1:
        threshold = (len(remaining) + 1) // 2
        current_col = tuple(row[current_col_idx] for row in remaining)
        selector = 1 if sum(current_col) >= threshold else 0
        remaining = tuple(row for bit, row in zip(current_col, remaining) if bit == selector)
        current_col_idx += 1
    return remaining[0]


def co2_scrubber_rating(matrix):
    remaining = tuple(tuple(row) for row in matrix)
    current_col_idx = 0
    while len(remaining) > 1:
        threshold = (len(remaining) + 1) // 2
        current_col = tuple(row[current_col_idx] for row in remaining)
        selector = 0 if sum(current_col) >= threshold else 1
        remaining = tuple(row for bit, row in zip(current_col, remaining) if bit == selector)
        current_col_idx += 1
    return remaining[0]


def life_support_rating(matrix):
    return decimal(oxygen_generator_rating(matrix)) * decimal(co2_scrubber_rating(matrix))


def part_1():
    return power(read_data())


def part_2():
    return life_support_rating(read_data())


def main():
    matrix = [[0, 0, 1, 0, 0],
              [1, 1, 1, 1, 0],
              [1, 0, 1, 1, 0],
              [1, 0, 1, 1, 1],
              [1, 0, 1, 0, 1],
              [0, 1, 1, 1, 1],
              [0, 0, 1, 1, 1],
              [1, 1, 1, 0, 0],
              [1, 0, 0, 0, 0],
              [1, 1, 0, 0, 1],
              [0, 0, 0, 1, 0],
              [0, 1, 0, 1, 0]]
    print(power(matrix))
    print(life_support_rating(matrix))


if __name__ == '__main__':
    main()
