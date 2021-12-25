from collections import defaultdict


def read_data():
    with open('puzzle24.in', 'r') as f:
        params = []
        for _ in range(14):
            pos_params = []
            for _ in range(4):
                next(f)
            pos_params.append(int(next(f).strip().split()[-1]))  # a
            pos_params.append(int(next(f).strip().split()[-1]))  # b
            for _ in range(9):
                next(f)
            pos_params.append(int(next(f).strip().split()[-1]))  # c
            for _ in range(2):
                next(f)
            params.append(pos_params)
    return params


def valid(new_z, a, b, c):
    result = defaultdict(set)
    for i in range(1, 10):
        target = new_z - c - i
        q, r = divmod(target, 26)
        if r == 0:
            if a == 1:
                result[i].add(q)
            else:  # a == 26
                result[i] |= set(range(target, target + 26))
        if a == 1:
            if new_z + b == i:
                result[i].add(new_z)
        else:  # a == 26
            result[i] |= {z for z in set(range(26 * new_z, 26 * (new_z + 1)))
                            if (z % 26) + b == i}
    return result


def search(params, zs=None, acc=0, depth=13, maximize=True):
    if depth < 0:
        return acc
    if zs is None:  # lowest level -> end with z == 0
        valid_inputs = valid(0, *params[depth])
    else:
        valid_inputs = defaultdict(set)
        for z in zs:
            for i, izs in valid(z, *params[depth]).items():
                valid_inputs[i] |= izs
    best = 0 if maximize else float('inf')
    for i, izs in valid_inputs.items():
        if not izs:
            continue
        new_acc = acc + i * pow(10, 13 - depth)
        result = search(params, izs, new_acc, depth - 1, maximize)
        if (maximize and result > best) or (not maximize and result < best):
            best = result
    return best


def part_1():
    return search(read_data())


def part_2():
    return search(read_data(), maximize=False)


def main():
    print(search(read_data()))
    print(search(read_data(), maximize=False))


if __name__ == '__main__':
    main()
