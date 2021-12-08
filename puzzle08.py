segments = {
    0: frozenset('abcefg'),
    1: frozenset('cf'),
    2: frozenset('acdeg'),
    3: frozenset('acdfg'),
    4: frozenset('bcdf'),
    5: frozenset('abdfg'),
    6: frozenset('abdefg'),
    7: frozenset('acf'),
    8: frozenset('abcdefg'),
    9: frozenset('abcdfg')
}

segments_lookup = {word: number for number, word in segments.items()}


def read_data():
    with open('puzzle08.in', 'r') as f:
        yield from (line.strip() for line in f)


def parse_line(line):
    inputs, outputs = line.split(' | ')
    return tuple([frozenset(word) for word in group.split()] for group in (inputs, outputs))


def part_1():
    total = 0
    for inputs, outputs in (parse_line(line) for line in read_data()):
        total += sum(1 for word in outputs if len(word) in (2, 3, 4, 7))
    return total


def decode_line(inputs, outputs):
    cf = [word for word in inputs if len(word) == 2][0]  # one
    acf = [word for word in inputs if len(word) == 3][0]  # seven
    a = acf - cf
    bcdf = [word for word in inputs if len(word) == 4][0]  # four
    bd = bcdf - cf
    abcdefg = [word for word in inputs if len(word) == 7][0]  # eight
    eg = abcdefg - acf - bd
    abdefg = [word for word in inputs if len(word) == 6 and abcdefg - word <= cf][0]  # six
    f = abdefg - a - bd - eg
    c = cf - f
    abcdfg = [word for word in inputs if len(word) == 6 and abcdefg - word <= eg][0]  # nine
    g = abcdfg - acf - bd
    e = eg - g
    acdeg = [word for word in inputs if len(word) == 5 and abcdefg - f - word <= bd][0]  # two
    d = acdeg - a - c - eg
    b = bd - d
    decoded_segments = {next(iter(encoded)): decoded
                        for encoded, decoded in zip((a, b, c, d, e, f, g), 'abcdefg')}
    decoded_outputs = [frozenset(decoded_segments[segment] for segment in word)
                       for word in outputs]
    output_numbers = [segments_lookup[word] for word in decoded_outputs]
    total = 0
    for number in output_numbers:
        total = 10 * total + number
    return total


def part_2():
    total = 0
    for inputs, outputs in (parse_line(line) for line in read_data()):
        total += decode_line(inputs, outputs)
    return total


def main():
    test_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
    total = 0
    for line in test_input.split('\n'):
        inputs, outputs = parse_line(line)
        total += sum(1 for word in outputs if len(word) in (2, 3, 4, 7))
    print(total)
    print('***')
    total = 0
    for line in test_input.split('\n'):
        inputs, outputs = parse_line(line)
        total += decode_line(inputs, outputs)
    print(total)
    print('---')
    inputs, outputs = parse_line("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    print(decode_line(inputs, outputs))

if __name__ == '__main__':
    main()
