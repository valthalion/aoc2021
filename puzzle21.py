from collections import Counter
from itertools import product
from random import randint


potential_rolls = Counter(sum(dice) for dice in product((1, 2, 3),
                                                        (1, 2, 3),
                                                        (1, 2, 3)))


def read_data():
    with open('puzzle21.in', 'r') as f:
        p1 = int(next(f).strip().split()[-1])
        p2 = int(next(f).strip().split()[-1])
    return p1, p2


class Die:
    def __init__(self, sides):
        self.count = 0
        self.sides = sides

    def roll(self):
        self.count += 1
        return randint(1, sides)


class DeterministicDie(Die):
    def __init__(self, sides):
        super().__init__(sides)
        self.last_roll = 0

    def roll(self):
        self.count += 1
        result = self.last_roll + 1
        if result > self.sides:
            result = 1
        self.last_roll = result
        return result


def play(p1, p2, rolls, target_score=1_000, board_size = 10):
    positions = {'p1': p1, 'p2': p2}
    scores = {'p1': 0, 'p2': 0}
    while True:
        for player in positions:
            roll = sum(rolls.roll() for _ in range(3))
            positions[player] = ((positions[player] + roll - 1) % board_size) + 1
            scores[player] += positions[player]
            if scores[player] >= target_score:
                return tuple(sorted(scores.values(), reverse=True))


def play_dirac(p1_pos, p2_pos, p1_score=0, p2_score=0, next_player=0):
    if p1_score >= 21:
        return (1, 0)
    if p2_score >= 21:
        return (0, 1)
    p1_wins, p2_wins = 0, 0
    for roll, multiplier in potential_rolls.items():
        if next_player == 0:  # p1's turn
            new_p1_pos, new_p2_pos = ((p1_pos + roll - 1) % 10) + 1, p2_pos
            new_p1_score, new_p2_score = p1_score + new_p1_pos, p2_score
        else:  # p2's turn
            new_p1_pos, new_p2_pos = p1_pos, ((p2_pos + roll - 1) % 10) + 1
            new_p1_score, new_p2_score = p1_score, p2_score + new_p2_pos
        new_p1_wins, new_p2_wins = play_dirac(new_p1_pos,
                                              new_p2_pos,
                                              new_p1_score,
                                              new_p2_score,
                                              1 - next_player)
        p1_wins += multiplier * new_p1_wins
        p2_wins += multiplier * new_p2_wins
    return p1_wins, p2_wins


def part_1():
    rolls = DeterministicDie(100)
    p1, p2 = read_data()
    score_winner, score_loser = play(p1, p2, rolls)
    return score_loser * rolls.count


def part_2():
    p1, p2 = read_data()
    p1_wins, p2_wins = play_dirac(p1, p2)
    return max(p1_wins, p2_wins)


def main():
    rolls = DeterministicDie(100)
    p1, p2 = 4, 8
    score_winner, score_loser = play(p1, p2, rolls, target_score=1_000, board_size = 10)
    print(score_loser * rolls.count, 739785)
    print(*play_dirac(p1, p2))
    print(444356092776315, 341960390180808)


if __name__ == '__main__':
    main()
