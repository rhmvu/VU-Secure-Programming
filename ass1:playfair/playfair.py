#!/usr/bin/env python

# Name: Ruben van der Ham
# VU net id: rhm270
# Student number: 2592271
# Email: 2592271@student.vu.nl

from __future__ import print_function
from collections import OrderedDict
import re
import sys

HELP_MESSAGE = """Playfair implementation by Ruben van der Ham\n
Usage: playfair.py <mode> key <plaintext/ciphertext>
mode:
\t -e: encrypts plaintext by the specified key
\t -d: decrypts ciphertext by the specified key
\t -h: displays this help message   """

FAILURE_MESSAGE = "Error occurred: {}\n\nFor help information run 'python playfair.py -h'"
PADDING_CHAR = "x"
GRID_SIZE = 5
alphabet = "abcdefghjklmnopqrstuvwxyz"


def main():
    try:
        func = parse_args()
    except Exception as e:
        print(print_fail(e))
        exit(1)

    # run the function/mode
    if func == return_help:
        result = func()
    else:
        try:
            result = func(sys.argv[2], sys.argv[3])
        except Exception as e:
            print(print_fail(e))
            exit(1)

    print(result)


def parse_args():
    # Check for parameters
    argc = len(sys.argv)
    if argc < 4 and sys.argv[1] != "-h":
        raise Exception("Not enough parameters")
    if argc > 4 and sys.argv[1] != "-h":
        raise Exception("Too much parameters")
    mode = {
        "-e": encrypt,
        "-d": decrypt,
        "-h": return_help
    }
    try:
        return mode[sys.argv[1]]
    except ValueError:
        raise Exception('Mode not found')


def print_fail(exception):
    fail_message = "Unknown error"
    if exception:
        fail_message = str(exception)
    return str.format(FAILURE_MESSAGE, fail_message)


def return_help():
    return HELP_MESSAGE


def encrypt(basekey, plain):
    key = generate_playfair_key(basekey)
    grid = build_grid(key)
    message = prepare_message(plain)

    cipher = ""
    for bigram in message:
        x_one, y_one = find_index(grid, bigram[0])
        x_two, y_two = find_index(grid, bigram[1])

        # if in same row
        if y_one == y_two:
            cipher = cipher + str(grid[(x_one+1) % GRID_SIZE][y_one])
            cipher = cipher + str(grid[(x_two+1) % GRID_SIZE][y_two])
            continue

        # if in the same column
        if x_one == x_two:
            cipher = cipher + str(grid[x_one][(y_one-1) % GRID_SIZE])
            cipher = cipher + str(grid[x_two][(y_two-1) % GRID_SIZE])
        else:
            cipher = cipher + str(grid[x_two][y_one])
            cipher = cipher + str(grid[x_one][y_two])
    return cipher


def decrypt(basekey, cipher):
    key = generate_playfair_key(basekey)
    grid = build_grid(key)

    # if cipher contains i replace by j, although this shouldn't happen with my program's encryption
    cipher = cipher.replace("i", "j")

    # detect incorrect cipher format
    if len(cipher) % 2 == 1:
        raise Exception("cipher has incorrect formatting: uneven amount of characters")

    cipher = re.findall("..", cipher)

    plain = ""
    for bigram in cipher:
        x_one, y_one = find_index(grid, bigram[0])
        x_two, y_two = find_index(grid, bigram[1])

        # if in same row
        if y_one == y_two:
            plain = plain + str(grid[(x_one-1) % GRID_SIZE][y_one])
            plain = plain + str(grid[(x_two-1) % GRID_SIZE][y_two])
            continue

        # if in the same column
        if x_one == x_two:
            plain = plain + str(grid[x_one][(y_one+1) % GRID_SIZE])
            plain = plain + str(grid[x_two][(y_two+1) % GRID_SIZE])
        else:
            plain = plain + str(grid[x_two][y_one])
            plain = plain + str(grid[x_one][y_two])

    # remove all instances of x
    plain = plain.replace("x", "")

    return plain


def prepare_message(plain):
    # prepare message
    if "x" in plain:
        raise Exception("Plain text may NOT contain character 'x'")

    plain = plain.replace("i", "j")

    # check for double characters:
    added = 0
    previous = ""
    charlist = []
    for i in range(0, len(plain)):
        if plain[i] == previous and i % 2 == (added+1) % 2:
            charlist.append(PADDING_CHAR)
            added += 1
        charlist.append(plain[i])
        previous = plain[i]

    # apply padding for odd length
    if len(charlist) % 2 == 1:
        charlist.append(PADDING_CHAR)  # apply padding

    return re.findall("..", "".join(charlist))


def find_index(grid, char):
    for y in range(0, GRID_SIZE):
        for x in range(0, GRID_SIZE):
            if grid[x][y] == char:
                return x, y
    raise Exception("Runtime error, couldn't find index in grid") #means there is a problem with the grid- or key construction


def generate_playfair_key(basekey):

    # replace al 'i's by 'j's (although assumed they are not present)
    basekey = basekey.replace("i", "j")

    # remove all double occurrences if present to correct mistakes (although assumed they are not present)
    basekey = "".join(OrderedDict.fromkeys(basekey))

    global alphabet
    restkey = list(alphabet)

    for char in basekey:
        restkey.remove(char)
    return basekey+"".join(restkey)


def build_grid(key):
    # initialize grid with None
    grid = [[None for n in range(GRID_SIZE)] for m in range(GRID_SIZE)]

    # Iterate over the grid to insert the whole key
    for y in range(0, GRID_SIZE):
        for x in range(0, GRID_SIZE):
            grid[x][GRID_SIZE-1-y] = key[GRID_SIZE*y+x]
    return grid


# DEBUG function #
def print_grid(grid):
    for y in range(0, GRID_SIZE):
        for x in range(0, GRID_SIZE):
            print(grid[x][4-y]+" ", end="")
        print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl+C: Quitting program")