from collections import Counter
from functools import wraps


def cached(f):
    cache = {}
    @wraps(f)
    def inner(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return inner


def read_data():
    with open('puzzle14.in', 'r') as f:
        template = next(f).strip()
        next(f)  # skip blank line
        insertions = {}
        for line in f:
            base, insertion = line.strip().split(' -> ')
            insertions[tuple(base)] = insertion
    return template, insertions


def process(template, insertions):
    last = None
    for monomer in template:
        base = (last, monomer)
        if base in insertions:
            yield insertions[base]
        last = monomer
        yield monomer


def process2(template, insertions, steps):
    @cached
    def pair_insertions(pair, steps):
        left, right = pair
        if steps == 0 or pair not in insertions:
            return ((left, 2),) if left == right else ((left, 1), (right, 1))
        insertion = insertions[pair]
        total_count = Counter()
        total_count.update(dict(pair_insertions((left, insertion), steps - 1)))
        total_count.update(dict(pair_insertions((insertion, right), steps - 1)))
        total_count[insertion] -= 1  # is included in both counts above
        return tuple(total_count.items())
    counts = Counter()
    for pair in zip(template, template[1:]):
        counts.update(dict(pair_insertions(pair, steps)))
    counts -= Counter(template[1:-1])  # remove double counting of internal monomers
    sorted_counts = counts.most_common()
    highest, lowest = sorted_counts[0][1], sorted_counts[-1][1]
    return highest - lowest


def count_difference(polymer):
    counts = Counter(polymer)
    sorted_counts = counts.most_common()
    highest, lowest = sorted_counts[0][1], sorted_counts[-1][1]
    return highest - lowest


def part_1():
    polymer, insertions = read_data()
    for _ in range(10):
        polymer = process(polymer, insertions)
    return count_difference(polymer)


def part_2():
    polymer, insertions = read_data()
    return process2(polymer, insertions, 40)


def main():
    template = 'NNCB'
    insertions = {
        ('C', 'H'): 'B',
        ('H', 'H'): 'N',
        ('C', 'B'): 'H',
        ('N', 'H'): 'C',
        ('H', 'B'): 'C',
        ('H', 'C'): 'B',
        ('H', 'N'): 'C',
        ('N', 'N'): 'C',
        ('B', 'H'): 'H',
        ('N', 'C'): 'B',
        ('N', 'B'): 'B',
        ('B', 'N'): 'B',
        ('B', 'B'): 'N',
        ('B', 'C'): 'B',
        ('C', 'C'): 'N',
        ('C', 'N'): 'C'
    }

    polymer = ''.join(process(template, insertions))
    print(' 1 step: ', polymer)
    polymer = ''.join(process(polymer, insertions))
    print(' 2 steps:', polymer)
    for _ in range(8):
        polymer = ''.join(process(polymer, insertions))
    print('10 steps:', count_difference(polymer))
    print('---')
    print('10 steps:', process2(template, insertions, 10), 1588)
    print('10 steps:', process2(template, insertions, 40), 2188189693529)


if __name__ == '__main__':
    main()
