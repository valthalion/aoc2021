def read_data():
    points = set()
    folds = []
    with open('puzzle13.in', 'r') as f:
        while (line := next(f).strip()):
            points.add(tuple(int(x) for x in line.split(',')))
        for line in f:
            fold = line.strip().split()[-1]
            axis, pos = fold.split('=')
            folds.append((axis, int(pos)))
    return points, folds


def do_fold(points, fold):
    fold_axis, fold_pos = fold
    if fold_axis == 'x':
        new_points = {point if point[0] < fold_pos else (2 * fold_pos - point[0], point[1])
                      for point in points}
    else:
        new_points = {point if point[1] < fold_pos else (point[0], 2 * fold_pos - point[1])
                      for point in points}
    return new_points


def show(points):
    rows = max(x for x, _ in points) + 1
    cols = max(y for _, y in points) + 1
    lines = (''.join('#' if (r, c) in points else ' ' for c in range(cols))
             for r in range(rows))
    return '\n'.join(lines)


def part_1():
    points, folds = read_data()
    points = do_fold(points, folds[0])
    return len(points)


def part_2():
    points, folds = read_data()
    for fold in folds:
        points = do_fold(points, fold)
    return show(points)


def main():
    points = {(6,10), (0,14), (9,10), (0,3), (10,4), (4,11), (6,0), (6,12), (4,1),
              (0,13), (10,12), (3,4), (3,0), (8,4), (1,10), (2,14), (8,10), (9,0)}
    folds = [('y', 7), ('x', 5)]
    points = do_fold(points, folds[0])
    print(len(points), 17)
    points = do_fold(points, folds[1])
    print(show(points))


if __name__ == '__main__':
    main()
