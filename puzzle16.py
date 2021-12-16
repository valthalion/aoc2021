from math import prod


hex2bin = {
    '0': (0, 0, 0, 0),
    '1': (0, 0, 0, 1),
    '2': (0, 0, 1, 0),
    '3': (0, 0, 1, 1),
    '4': (0, 1, 0, 0),
    '5': (0, 1, 0, 1),
    '6': (0, 1, 1, 0),
    '7': (0, 1, 1, 1),
    '8': (1, 0, 0, 0),
    '9': (1, 0, 0, 1),
    'A': (1, 0, 1, 0),
    'B': (1, 0, 1, 1),
    'C': (1, 1, 0, 0),
    'D': (1, 1, 0, 1),
    'E': (1, 1, 1, 0),
    'F': (1, 1, 1, 1)
}


def take(source, n):
    yield from [next(source) for _ in range(n)]


def read_data():
    with open('puzzle16.in', 'r') as f:
        return next(f).strip()


def hex_to_bin(stream):
    for c in stream:
        yield from hex2bin[c] 


def read_bin(source, length):
    total = 0
    for _ in range(length):
        total <<= 1
        total += next(source)
    return total


def read_literal(source):
    total, length = 0, 0
    while True:
        lead = next(source)
        total <<= 4
        total += read_bin(source, 4)
        length += 5
        if lead == 0:
            break
    return total


def read_packet(source):
    version = read_bin(source, 3)
    packet_type = read_bin(source, 3)
    packet = {'version': version, 'type': packet_type}

    if packet_type == 4:  # Literal value
        packet['value'] = read_literal(source)
        return packet
    
    length_type = next(source)
    if length_type == 0:  # total length of subpackets (15 bits)
        subpackets_length = read_bin(source, 15)
        new_source = take(source, subpackets_length)
        packet['subpackets'] = []
        while True:
            try:
                next_packet = read_packet(new_source)
            except StopIteration:
                break
            packet['subpackets'].append(next_packet)
    else:  # number of subpackets (11 bits)
        n_subpackets = read_bin(source, 11)
        packet['subpackets'] = [read_packet(source) for _ in range(n_subpackets)]
    return packet


def sum_versions(packet):
    total = packet['version']
    if 'subpackets' in packet:
        for subpacket in packet['subpackets']:
            total += sum_versions(subpacket)
    return total


def eval_packet(packet):
    if packet['type'] == 4:
        return packet['value']
    operator = packet['type']
    subpackets = packet['subpackets']
    if operator == 0:
        return sum(eval_packet(subpacket) for subpacket in subpackets)
    if operator == 1:
        return prod(eval_packet(subpacket) for subpacket in subpackets)
    if operator == 2:
        return min(eval_packet(subpacket) for subpacket in subpackets)
    if operator == 3:
        return max(eval_packet(subpacket) for subpacket in subpackets)
    if operator == 5:
        return 1 if eval_packet(subpackets[0]) > eval_packet(subpackets[1]) else 0
    if operator == 6:
        return 1 if eval_packet(subpackets[0]) < eval_packet(subpackets[1]) else 0
    if operator == 7:
        return 1 if eval_packet(subpackets[0]) == eval_packet(subpackets[1]) else 0


def part_1():
    stream = read_data()
    packet = read_packet(hex_to_bin(stream))
    return sum_versions(packet)


def part_2():
    stream = read_data()
    packet = read_packet(hex_to_bin(stream))
    return eval_packet(packet)


def main():
    literal = tuple(int(c) for c in '110100101111111000101000')
    print(read_packet(iter(literal)), 'Literal: 2021')
    operator = tuple(int(c) for c in '00111000000000000110111101000101001010010001001000000000')
    print(read_packet(iter(operator)), 'operator: 6; Literal: 10; Literal: 20')
    operator = tuple(int(c) for c in '11101110000000001101010000001100100000100011000001100000')
    print(read_packet(iter(operator)), 'operator: 3; Literal: 1; Literal: 2; Literal: 3')

    stream = '8A004A801A8002F478'
    packet = read_packet(hex_to_bin(stream))
    print('---')
    print(packet)
    print(sum_versions(packet), 16)

    stream = '620080001611562C8802118E34'
    packet = read_packet(hex_to_bin(stream))
    print('---')
    print(packet)
    print(sum_versions(packet), 12)

    stream = 'C0015000016115A2E0802F182340'
    packet = read_packet(hex_to_bin(stream))
    print('---')
    print(packet)
    print(sum_versions(packet), 23)

    stream = 'A0016C880162017C3686B18A3D4780'
    packet = read_packet(hex_to_bin(stream))
    print('---')
    print(packet)
    print(sum_versions(packet), 31)

    print('\n***\n')

    stream = 'C200B40A82'
    print(eval_packet(read_packet(hex_to_bin(stream))), 3)
    stream = '04005AC33890'
    print(eval_packet(read_packet(hex_to_bin(stream))), 54)
    stream = '880086C3E88112'
    print(eval_packet(read_packet(hex_to_bin(stream))), 7)
    stream = 'CE00C43D881120'
    print(eval_packet(read_packet(hex_to_bin(stream))), 9)
    stream = 'D8005AC2A8F0'
    print(eval_packet(read_packet(hex_to_bin(stream))), 1)
    stream = 'F600BC2D8F'
    print(eval_packet(read_packet(hex_to_bin(stream))), 0)
    stream = '9C005AC2F8F0'
    print(eval_packet(read_packet(hex_to_bin(stream))), 0)
    stream = '9C0141080250320F1802104A08'
    print(eval_packet(read_packet(hex_to_bin(stream))), 1)


if __name__ == '__main__':
    main()
