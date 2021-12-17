from math import sqrt
import re


target_re = re.compile(r'''target area: x=(?P<x1>\-?\d+)..(?P<x2>\-?\d+), y=(?P<y1>\-?\d+)..(?P<y2>\-?\d+)''')
inf = float('inf')


def read_data():
    with open('puzzle17.in', 'r') as f:
        target = next(f).strip()
        m = target_re.match(target)
        x1 = int(m.group('x1'))
        x2 = int(m.group('x2'))
        y1 = int(m.group('y1'))
        y2 = int(m.group('y2'))
    return {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2}


def height(v):
    return (v * (v + 1)) // 2 if v > 0 else 0


def inverse_height(h):
    return int((sqrt(1 + 8 * h) - 1) / 2)


def horizontal_intersections(v, target):
    pos, step = 0, 0
    intersections = set()
    while pos <= target['x2'] and v > 0:
        pos += v
        step += 1
        if target['x1'] <= pos <= target['x2']:
            intersections.add(step)
        v -= 1
    if v == 0 and target['x1'] <= pos <= target['x2']:
        intersections.add(inf)
    return intersections


def horizontal_trajectories(target):
    min_vx = inverse_height(target['x1'])
    max_vx = target['x2'] + 1
    trajectories = {}
    for vx in range(min_vx, max_vx):
        in_target = horizontal_intersections(vx, target)
        if in_target:
            trajectories[vx] = in_target
    return trajectories


def vertical_intersections(v, target):
    pos, step = 0, 0
    intersections = set()
    while pos >= target['y1'] or v > 0:
        pos += v
        step += 1
        if target['y1'] <= pos <= target['y2']:
            intersections.add(step)
        v -= 1
    return intersections


def vertical_trajectories(target):
    min_vy = target['y1']
    max_vy = 125  # TODO: Calculate this
    trajectories = {}
    for vy in range(min_vy, max_vy):
        in_target = vertical_intersections(vy, target)
        if in_target:
            trajectories[vy] = in_target
    return trajectories


def intersect(stepsx, stepsy):
    if stepsx & stepsy:
        return True
    if inf in stepsx:
        if max(stepsx - {inf}) < max(stepsy):
            return True
    return False


def all_shots(target):  # vy = 124, 7750
    for vx, hor_steps in horizontal_trajectories(target).items():
        for vy, vert_steps in vertical_trajectories(target).items():
            if intersect(hor_steps, vert_steps):
                yield vx, vy


def highest_shot(target):
    max_vy = max(vy for _vx, vy in all_shots(target))
    return height(max_vy)


def part_1():
    return highest_shot(read_data())


def part_2():
    return sum(1 for _ in all_shots(read_data()))


def main():
    target = {'x1': 20, 'x2': 30, 'y1': -10, 'y2': -5}
    print(highest_shot(target), 45)
    print(sum(1 for _ in all_shots(target)), 112)


if __name__ == '__main__':
    main()
