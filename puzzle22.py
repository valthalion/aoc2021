from itertools import product
from math import prod


class Cuboid:
    @classmethod
    def from_spec(cls, spec):
        x, y, z = (part[2:] for part in spec.split(','))
        xmin, xmax = (int(n) for n in x.split('..'))
        ymin, ymax = (int(n) for n in y.split('..'))
        zmin, zmax = (int(n) for n in z.split('..'))
        return cls((xmin, ymin, zmin), (xmax + 1, ymax + 1, zmax + 1))

    def __init__(self, mins, maxs):
        self.mins = mins
        self.maxs = maxs

    def points(self, filter=(None, None)):
        return set(product(*(range(max(low, filter[0]), min(high, filter[1] + 1))
                             for low, high in self)))

    def __len__(self):
        return prod(high - low for low, high in self)

    def __contains__(self, other):
        return all((self_min <= other_min and self_max >= other_max)
                   for (self_min, self_max), (other_min, other_max) in zip(self, other))

    def __iter__(self):
        yield from zip(self.mins, self.maxs)

    def __sub__(self, other):
        if self in other:
            return set()
        if not self.intersects(other):
            return {self}

        previous = {self}
        for dim, (other_min, other_max) in enumerate(other):
            current = set()
            for cuboid in previous:
                cuboid_min, cuboid_max = cuboid.mins[dim], cuboid.maxs[dim]
                if other_min <= cuboid_min and other_max >= cuboid_max:
                    current.add(cuboid)
                elif other_min >= cuboid_min and other_max <= cuboid_max:
                    current |= cuboid.partition(dim, (other_min, other_max))
                elif other_min >= cuboid_min:
                    current |= cuboid.partition(dim, (other_min,))
                else:  # other_min >= cuboid_min
                    current |= cuboid.partition(dim, (other_max,))
            previous = current
        return {cuboid for cuboid in current if not cuboid.intersects(other)}

    def partition(self, dim, breaking_points):
        endpoints = [self.mins[dim], *breaking_points, self.maxs[dim]]
        intervals = zip(endpoints, endpoints[1:])
        return {Cuboid(tuple(low if dim == step else self_low
                             for step, self_low in enumerate(self.mins)),
                       tuple(high if dim == step else self_high
                             for step, self_high in enumerate(self.maxs)))
                for low, high in intervals}

    def intersects(self, other):
        return all((other_min < self_max and other_max > self_min)
                   for (self_min, self_max), (other_min, other_max) in zip(self, other))


class Reactor:
    def __init__(self):
        self.on = set()

    def __len__(self): return sum(len(cuboid) for cuboid in self.on)

    def __add__(self, cuboid):
        remove_cuboid_points = self - cuboid
        remove_cuboid_points.on.add(cuboid)
        return remove_cuboid_points

    def __sub__(self, cuboid):
        if not self.on:
            return self
        intersections = {other_cuboid
                         for other_cuboid in self.on
                         if other_cuboid.intersects(cuboid)}
        self.on -= intersections
        for other_cuboid in intersections:
            self.on |= other_cuboid - cuboid
        return self


def read_data(test=False):
    filename = f'puzzle22-test{test}.in' if test else 'puzzle22.in'
    with open(filename, 'r') as f:
        for line in f:
            cmd, cuboid_spec = line.strip().split()
            yield cmd, Cuboid.from_spec(cuboid_spec)


def initialize(cmd_seq):
    reactor = set()
    for cmd, cuboid in cmd_seq:
        if cmd == 'on':
            reactor |= cuboid.points(filter=(-50, 50))
        else:
            reactor -= cuboid.points(filter=(-50, 50))
    return reactor


def reboot(cmd_seq):
    reactor = Reactor()
    for cmd, cuboid in cmd_seq:
        if cmd == 'on':
            reactor += cuboid
        else:
            reactor -= cuboid
    return reactor


def part_1():
    return len(initialize(read_data()))


def part_2():
    return len(reboot(read_data()))


def main():
    print(len(initialize(read_data(test=1))), 590784)
    print(len(initialize(read_data(test=2))), 474140)
    print(len(reboot(read_data(test=2))))
    print(2758514936282235)


if __name__ == '__main__':
    main()
