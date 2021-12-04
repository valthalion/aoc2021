from collections import defaultdict

from puzzle03 import transpose


def read_data():
    with open('puzzle04.in', 'r') as f:
        numbers = [int(x) for x in next(f).strip().split(',')]
        next(f)  # skip blank line

        boards = []
        current_board = []
        for line in f:
            if line == '\n':
                boards.append(current_board)
                current_board = []
                continue
            current_board.append([int(x) for x in line.strip().split()])
        if current_board:  # needed if there is no blank line at the end of the input
            boards.append(current_board)
        return boards, numbers


def play(boards, numbers, to_win=True):
    number_placements = defaultdict(set)
    rows_marked = [[0] * 5 for _ in range(len(boards))]
    cols_marked = [[0] * 5 for _ in range(len(boards))]
    for b, board in enumerate(boards):
        for r, row in enumerate(board):
            for c, number in enumerate(row):
                number_placements[number].add((b, r, c))
    marked = set()
    winners = set()
    remaining = set(range(len(boards)))
    last_number = None
    last_remaining = None
    for number in numbers:
        marked.add(number)
        if number in number_placements:
            for b, r, c in number_placements[number]:
                rows_marked[b][r] += 1
                if rows_marked[b][r] == 5:
                    winners.add(b)
                cols_marked[b][c] += 1
                if cols_marked[b][c] == 5:
                    winners.add(b)
            if not to_win:
                if len(remaining) == 1 and remaining <= winners:
                    last_remaining = remaining.pop()
            remaining -= winners
            if (to_win and winners) or (not to_win and len(remaining) == 0):
                last_number = number
                break
    if (to_win and len(winners) != 1) or (not to_win and last_remaining is None):
        raise RuntimeError('No winner or tied boards / wrong number remaining:', winners, remaining)
    selected = winners.pop() if to_win else last_remaining
    selected_score = sum({x for row in boards[selected] for x in row} - marked)
    return last_number, selected_score


def part_1():
    boards, numbers = read_data()
    last_number, winner_score = play(boards, numbers)
    return last_number * winner_score


def part_2():
    boards, numbers = read_data()
    last_number, loser_score = play(boards, numbers, to_win=False)
    return last_number * loser_score


def main():
    numbers = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16,
               13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]
    boards = [
        [[22, 13, 17, 11, 0],
         [8, 2, 23, 4, 24],
         [21, 9, 14, 16, 7],
         [6, 10, 3, 18, 5],
         [1, 12, 20, 15, 19]],

        [[3, 15, 0, 2, 22],
         [9, 18, 13, 17, 5],
         [19, 8, 7, 25, 23],
         [20, 11, 10, 24, 4],
         [14, 21, 16, 12, 6]],

        [[14, 21, 17, 24, 4],
         [10, 16, 15, 9, 19],
         [18, 8, 23, 26, 20],
         [22, 11, 13, 6, 5],
         [2, 0, 12, 3, 7]]
    ]

    last_number, winner_score = play(boards, numbers)
    print(last_number * winner_score)
    last_number, loser_score = play(boards, numbers, to_win=False)
    print(last_number * loser_score)


if __name__ == '__main__':
    main()
