from functools import reduce
from operator import add


def read_data():
    with open('puzzle18.in', 'r') as f:
        for line in f:
            yield eval(line.strip())


class Number:
    def __init__(self, number, depth = 0):
        self.depth = depth
        if isinstance(number, list):
            self.value = None
            left, right = number
            self.left = Number(left, depth=depth + 1)
            self.right = Number(right, depth=depth + 1)
        else:
            self.value = number
            self.left = self.right = None

    def magnitude(self):
        if self.value is None:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()
        return self.value

    def set_depth(self, depth):
        self.depth = depth
        if self.value is None:
            self.left.set_depth(depth + 1)
            self.right.set_depth(depth + 1)

    def split(self):
        value = self.value
        if value is None:
            if self.left.split():
                return True
            if self.right.split():
                return True
            return False
        if value < 10:
            return False
        new_depth = self.depth + 1
        left = value // 2
        right = value - left
        self.value, self.left, self.right = None, Number(left, new_depth), Number(right, new_depth)
        return True

    def leaves(self):
        if self.value is not None or self.depth > 3:
            yield self
            return
        yield from self.left.leaves()
        yield from self.right.leaves()

    def add_to_first_value(self, value):
        if self.value is not None:
            self.value += value
        else:
            self.left.add_to_first_value(value)

    def explode(self):
        leaves = list(self.leaves())
        for idx, leaf in enumerate(leaves):
            if leaf.value is None:
                left, right = leaf.left.value, leaf.right.value
                if idx > 0:
                    leaves[idx - 1].value += left
                if idx < len(leaves) - 1:
                    leaves[idx + 1].add_to_first_value(right)
                leaf.left = leaf.right = None
                leaf.value = 0
                return True
        return False

    def reduce(self):
        changes = True
        while changes:
            while self.explode():
                pass
            changes = self.split()

    def __add__(self, other):
        root = Number(None)
        self.set_depth(root.depth + 1)
        other.set_depth(root.depth + 1)
        root.left, root.right = self.copy(), other.copy()
        root.reduce()
        return root

    def copy(self):
        mycopy = Number(None, depth=self.depth)
        mycopy.value = self.value
        if self.value is None:
            mycopy.left = self.left.copy()
            mycopy.right = self.right.copy()
        return mycopy

    def __repr__(self, quiet=False):
        if self.value is not None:
            return str(self.value)
        if quiet:
           return f'[{self.left.__repr__(quiet=True)}, {self.right.__repr__(quiet=True)}]'
        return f'[{self.left.__repr__(quiet=True)}, {self.right.__repr__(quiet=True)}] ({self.max_depth()})'

    def max_depth(self):
        if self.value is not None:
            return self.depth
        return max(self.left.max_depth(), self.right.max_depth())

    def __str__(self):
        return self.__repr__()


def add_numbers(numbers):
    total = next(numbers)
    for number in numbers:
        total += number
    return total


def largest_magnitude(numbers):
    best = 0
    for idx, n1 in enumerate(numbers):
        for n2 in numbers[idx + 1:]:
            magnitude = (n1 + n2).magnitude()
            if magnitude > best:
                best = magnitude
            magnitude = (n2 + n1).magnitude()
            if magnitude > best:
                best = magnitude
    return best


def part_1():
    numbers = (Number(number) for number in read_data())
    total = add_numbers(numbers)
    return total.magnitude()


def part_2():
    numbers = list(Number(number) for number in read_data())
    return largest_magnitude(numbers)


def main():
    number_specs = (
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
        [[[5,[2,8]],4],[5,[[9,9],0]]],
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
        [[[[5,4],[7,7]],8],[[8,3],8]],
        [[9,3],[[9,9],[6,[4,9]]]],
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    )
    numbers = list(Number(number) for number in number_specs)
    for number_spec, number in zip(number_specs, numbers):
        print()
        print(number_spec)
        print(number)

    print('\n---\n')

    print(Number([1,2]) + Number([[3,4],5]))
    print('[[1, 2], [[3, 4], 5]]')

    print('\n---\n')

    n = Number([[[[[9,8],1],2],3],4])
    n.reduce()
    print(n)
    print('[[[[0, 9], 2], 3], 4]')
    print()

    n = Number([7,[6,[5,[4,[3,2]]]]])
    n.reduce()
    print(n)
    print('[7, [6, [5, [7, 0]]]]')
    print()

    n = Number([[6,[5,[4,[3,2]]]],1])
    n.reduce()
    print(n)
    print('[[6, [5, [7, 0]]], 3]')
    print()

    n = Number([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    n.reduce()
    print(n)
    print('[[3, [2, [8, 0]]], [9, [5, [7, 0]]]]')

    print('\n---\n')

    test = (
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
        [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
        [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
        [7,[5,[[3,8],[1,4]]]],
        [[2,[2,2]],[8,[8,1]]],
        [2,9],
        [1,[[[9,3],9],[[9,0],[0,7]]]],
        [[[5,[7,4]],7],1],
        [[[[4,2],2],6],[8,7]]
    )
    test_numbers = (Number(number) for number in test)
    total = add_numbers(test_numbers)
    print('[[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]')

    total = add_numbers(iter(numbers))
    print(total.magnitude(), 4140)

    print()
    largest = largest_magnitude(numbers)
    print(largest, 3993)


if __name__ == '__main__':
    main()
