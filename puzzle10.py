openings = {'(': ')', '[': ']', '{': '}', '<': '>'}
closings = {')': '(', ']': '[', '}': '{','>': '<'}
invalid_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
valid_scores = {')': 1, ']': 2, '}': 3, '>': 4}


def read_data():
    with open('puzzle10.in', 'r') as f:
        for line in f:
            yield line.strip()


def stack_score(stack):
    total_score = 0
    while stack:
        total_score = total_score * 5 + valid_scores[openings[stack.pop()]]
    return total_score


def parse_line(line):
    stack = []
    for c in line:
        if c in openings:
            stack.append(c)
        elif c in closings:
            if stack[-1] == closings[c]:
                stack.pop()
            else:
                return False, invalid_scores[c]
        else:
            raise RuntimeError('Invalid token')
    return True, stack_score(stack)


def median(v):
    half_pos = len(v) // 2
    return sorted(v)[half_pos]


def part_1():
    total_score = 0
    for line in read_data():
        valid, score = parse_line(line)
        if not valid:
            total_score += score
    return total_score


def part_2():
    parsed_lines = (parse_line(line) for line in read_data())
    print(median([score for valid, score in parsed_lines if valid]))


def main():
    test_input = r'''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''.split('\n')
    total_score = 0
    for line in test_input:
        valid, score = parse_line(line)
        if not valid:
            total_score += score
    print(total_score)
    print('---')
    parsed_lines = (parse_line(line) for line in test_input)
    print(median([score for valid, score in parsed_lines if valid]))


if __name__ == '__main__':
    main()
