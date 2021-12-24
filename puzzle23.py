from collections import defaultdict


target = dict(zip('ABCD', range(4)))
multiplier = dict(zip('ABCD', (1, 10, 100, 1_000)))

costs = {
    0: {0: 3, 1: 5, 2: 7, 3: 9},
    1: {0: 2, 1: 4, 2: 6, 3: 8},
    2: {0: 2, 1: 2, 2: 4, 3: 6},
    3: {0: 4, 1: 2, 2: 2, 3: 4},
    4: {0: 6, 1: 4, 2: 2, 3: 2},
    5: {0: 8, 1: 6, 2: 4, 3: 2},
    6: {0: 9, 1: 7, 2: 5, 3: 3}
}
constraints = {
    0: {0: {1}, 1: {1, 2}, 2: {1, 2, 3}, 3: {1, 2, 3, 4}},
    1: {0: set(), 1: {2}, 2: {2, 3}, 3: {2, 3, 4}},
    2: {0: set(), 1: set(), 2: {3}, 3: {3, 4}},
    3: {0: {2}, 1: set(), 2: set(), 3: {4}},
    4: {0: {2, 3}, 1: {3}, 2: set(), 3: set()},
    5: {0: {2, 3, 4}, 1: {3, 4}, 2: {4}, 3: set()},
    6: {0: {2, 3, 4, 5}, 1: {3, 4, 5}, 2: {4, 5}, 3: {5}}
}
direct_constraints = {
    0: {1: {2}, 2: {2, 3}, 3: {2, 3, 4}},
    1: {0: {2}, 2: {3}, 3: {3, 4}},
    2: {0: {2, 3}, 1: {3}, 3: {4}},
    3: {0: {2, 3, 4}, 1: {3, 4}, 2: {4}}
}


def read_data(test=False, insert_rows=False):
    filename = 'puzzle23-test.in' if test else 'puzzle23.in'
    with open(filename, 'r') as f:
        next(f)
        next(f)
        if not insert_rows:
            return tuple(zip(
                    (c for c in next(f) if c in 'ABCD'),
                    (c for c in next(f) if c in 'ABCD')
                ))
        return tuple(zip(
                (c for c in next(f) if c in 'ABCD'),
                'DCBA',
                'DBAC',
                (c for c in next(f) if c in 'ABCD')
            ))


def build_move(pos, move_type, hw_idx, room_idx, depth):
    move_cost = multiplier[pos] * (costs[hw_idx][room_idx] + depth)
    return (move_cost, move_type, hw_idx, room_idx, depth)


def hallway_moves(rooms, hallway):
    for hw_idx, pos in enumerate(hallway):
        if pos is None:
            continue

        room_idx = target[pos]
        if any(hallway[other_pos] is not None
               for other_pos in constraints[hw_idx][room_idx]):
            continue

        room = rooms[room_idx]
        for depth in reversed(range(len(room))):
            room_pos = room[depth]
            if room_pos is None or room_pos != pos:
                break
        if room_pos is None:
            yield build_move(pos, 'h', hw_idx, room_idx, depth)


def room_moves(rooms, hallway):
    for room_idx, room in enumerate(rooms):
        for depth, pos in enumerate(room):
            if pos is None:
                continue
            if room_idx == target[pos] and all(r == pos for r in room[depth + 1:]):
                break
            for hw_idx, hw_pos in enumerate(hallway):
                if hw_pos is not None:
                    continue
                if all(hallway[other_pos] is None
                       for other_pos in constraints[hw_idx][room_idx]):
                    yield build_move(pos, 'r', hw_idx, room_idx, depth)
            break

def moves(rooms, hallway):
    yield from hallway_moves(rooms, hallway)
    yield from room_moves(rooms, hallway)


def apply_move(move, rooms, hallway, cost):
    move_cost, origin, hw_idx, room_idx, depth = move
    room = rooms[room_idx]
    if origin == 'h':  # hallway to room
        pos = hallway[hw_idx]
        new_hallway = (*hallway[:hw_idx], None, *hallway[hw_idx + 1:])
        new_room = (*room[:depth], pos, *room[depth + 1:])
    else:  # room to hallway
        pos = room[depth]
        new_hallway = (*hallway[:hw_idx], pos, *hallway[hw_idx + 1:])
        new_room = (*room[:depth], None, *room[depth + 1:])
    new_rooms = (*rooms[:room_idx], new_room, *rooms[room_idx + 1:])
    return new_rooms, new_hallway, cost + move_cost


def lower_bound(rooms, hallway, base_cost):
    total = base_cost
    for room_idx, room in enumerate(rooms):
        for depth, pos in enumerate(room):
            if pos is None:
                continue
            target_room = target[pos]
            if room_idx != target_room or any(r != pos for r in room if r is not None):
                total += multiplier[pos] * (abs(target_room - room_idx) + depth + 3)
    for hw_idx, pos in enumerate(hallway):
        if pos is None:
            continue
        room_idx = target[pos]
        total += multiplier[pos] * (costs[hw_idx][room_idx])
    return total


def solve(rooms, hallway=(None,) * 7, accumulated_cost=0, best_cost=float('inf')):
    if all(room[0] is not None and room_idx == target[room[0]]
           for room_idx, room in enumerate(rooms)):
        return accumulated_cost
    potential_moves = sorted(moves(rooms, hallway))
    if not potential_moves:
        return float('inf')
    for move in potential_moves:
        new_rooms, new_hallway, new_acc_cost = apply_move(move, rooms, hallway, accumulated_cost)
        if lower_bound(new_rooms, new_hallway, new_acc_cost) >= best_cost:  # prune
            continue
        new_cost = solve(new_rooms, new_hallway, new_acc_cost, best_cost)
        if new_cost < best_cost:
            best_cost = new_cost

    return best_cost


def part_1():
    starting_state = read_data()
    return solve(rooms=starting_state)


def part_2():
    starting_state = read_data(insert_rows=True)
    return solve(rooms=starting_state)


def main():
    starting_state = read_data(test=True)
    print(solve(rooms=starting_state), 12521)
    starting_state = read_data(test=True, insert_rows=True)
    print(solve(rooms=starting_state), 44169)


if __name__ == '__main__':
    main()
