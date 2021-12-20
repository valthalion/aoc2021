charmap = {'.': 0, '#': 1}


def read_data(test=False):
    filename = 'puzzle20-test.in' if test else 'puzzle20.in'
    with open(filename, 'r') as f:
        img_enh = [charmap[c] for c in next(f).strip()]
        next(f)
        input_img = set()
        for r, line in enumerate(f):
            for c, pixel in enumerate(line.strip()):
                if charmap[pixel] == 1:
                    input_img.add((r, c))
    return input_img, img_enh


def bounding_box(img):
    minr, maxr, minc, maxc = float('inf'), float('-inf'), float('inf'), float('-inf')
    for r, c in img:
        if r < minr:
            minr = r
        if r > maxr:
            maxr = r
        if c < minc:
            minc = c
        if c > maxc:
            maxc = c
    return minr, maxr, minc, maxc


def display(img, inverted=False):
    minr, maxr, minc, maxc = bounding_box(img)
    off = '#' if inverted else '.'
    on = '.' if inverted else '#'
    for row in range(minr, maxr + 1):
        print(''.join(on if (row, col) in img else off for col in range(minc, maxc + 1)))
    print()


def mask(r, c):
    for row in range(r - 1, r + 2):
        for col in range(c - 1, c + 2):
            yield (row, col)


def binary(seq, complement=False):
    total = 0
    for n in seq:
        total *= 2
        total += (1 - n) if complement else n
    return total


def img_pass(img, img_enh, inverted=False, invert=False):
    invert_output = invert and not inverted
    minr, maxr, minc, maxc = bounding_box(img)
    newimg = set()
    for r in range(minr - 1, maxr + 2):
        for c in range(minc - 1, maxc + 2):
            output = img_enh[
                binary((1 if pixel in img else 0 for pixel in mask(r, c)), inverted)
            ]
            if (output == 0 and invert_output) or (output == 1 and not invert_output):
                newimg.add((r, c))
    return newimg


def process_img(img, img_enh, passes):
    inverted = False
    invert = (img_enh[0] == 1 and img_enh[-1] == 0)
    if invert and passes % 2 != 0:
        print('Output image will be inverted')
    for _ in range(passes):
        img = img_pass(img, img_enh, inverted, invert)
        if invert:
            inverted = not inverted
    return img


def part_1():
    img, img_enh = read_data()
    img = process_img(img, img_enh, passes=2)
    return len(img)


def part_2():
    img, img_enh = read_data()
    img = process_img(img, img_enh, passes=50)
    display(img)
    return len(img)


def main():
    img, img_enh = read_data(test=True)
    img = process_img(img, img_enh, passes=2)
    print(len(img), 35)
    img = process_img(img, img_enh, passes=48)
    print(len(img), 3351)
    display(img)


if __name__ == '__main__':
    main()
