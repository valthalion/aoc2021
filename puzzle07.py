def read_data():
    with open('puzzle07.in', 'r') as f:
        return [int(n) for n in next(f).strip().split(',')]


def total_dist(v, p):
    return sum(abs(x - p) for x in v)


def discrete_median(v):
    n = len(v)
    sorted_v = sorted(v)
    half_pos = n // 2
    median = sorted_v[half_pos]
    if n % 2 == 0:
        median = (median + sorted_v[half_pos - 1]) / 2
    return total_dist(v, median), median


def total_fuel(v, p):
    return sum((d * (d + 1)) // 2 for d in (abs(x - p) for x in v))


def bisection(v):
    low, high = min(v), max(v)
    middle = (low + high) // 2
    while low < high - 1:
        fmiddle = total_fuel(v, middle)
        fmiddle_right = total_fuel(v, middle + 1)
        fmiddle_left = total_fuel(v, middle - 1)
        if fmiddle <= fmiddle_right:
            if fmiddle <= fmiddle_left:
                break
            high = middle
        else:
            low = middle
        middle = (low + high) // 2
    return fmiddle, middle


def part_1():
    sum_dist, median = discrete_median(read_data())
    return sum_dist


def part_2():
    fuel, position = bisection(read_data())
    return fuel


def main():
    crabs = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    print(discrete_median(crabs))
    print(bisection(crabs))


if __name__ == '__main__':
    main()
