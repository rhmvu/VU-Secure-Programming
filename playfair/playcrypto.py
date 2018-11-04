from __future__ import print_function
from collections import OrderedDict
import re #regex

PADDING_CHAR = "x"
GRID_SIZE = 5
alphabet = "abcdefghjklmnopqrstuvwxyz"


def encrypt(basekey, plain):
    key = generate_playfair_key(basekey)
    grid = build_grid(key)
    message = prepare_message(plain)

    cipher = ""
    for bigram in message:
        x_one,y_one = find_index(grid,bigram[0])
        x_two,y_two = find_index(grid,bigram[1])

        #if in same row
        if y_one == y_two:
            cipher = cipher + str(grid[(x_one+1)%GRID_SIZE][y_one])
            cipher = cipher + str(grid[(x_two+1)%GRID_SIZE][y_two])
            continue

        # if in the same column
        if x_one == x_two:
            cipher = cipher + str(grid[x_one][(y_one-1)%GRID_SIZE])
            cipher = cipher + str(grid[x_two][(y_two-1)%GRID_SIZE])
        else:
            cipher = cipher + str(grid[x_two][y_one])
            cipher = cipher + str(grid[x_one][y_two])
    return cipher



def decrypt(basekey, cipher):
    key = generate_playfair_key(basekey)
    grid = build_grid(key)

    cipher = cipher.replace("i","j")
    if(len(cipher)%2==1):
        cipher+="x"


    cipher = re.findall("..",cipher)

    plain = ""
    for bigram in cipher:
        x_one,y_one = find_index(grid,bigram[0])
        x_two,y_two = find_index(grid,bigram[1])

        #if in same row
        if y_one == y_two:
            plain = plain + str(grid[(x_one-1)%GRID_SIZE][y_one])
            plain = plain + str(grid[(x_two-1)%GRID_SIZE][y_two])

            #print(bigram+"--->>"+plain[-3:-1])
            continue

        # if in the same column
        if x_one == x_two:
            plain = plain + str(grid[x_one][(y_one+1)%GRID_SIZE])
            plain = plain + str(grid[x_two][(y_two+1)%GRID_SIZE])
        else:
            plain = plain + str(grid[x_two][y_one])
            plain = plain + str(grid[x_one][y_two])
            #print(bigram+"--->>"+plain[-2:])

    #remove all occurencies of x
    plain = plain.replace("x","")

    return plain




def prepare_message(plain):
    #prepare message
    if "x" in plain:
        raise Exception("Plain text may NOT contain character 'x'")

    plain = plain.replace("i","j")

    #check for double characters:
    added = 0
    previous = ""
    charlist = []
    for i in range(0,len(plain)):
        if plain[i] == previous and i%2==(added+1)%2:
            charlist.append(PADDING_CHAR)
            added+=1
        charlist.append(plain[i])
        previous = plain[i]


    #apply padding for odd length
    if len(charlist) %2 == 1:
        charlist.append(PADDING_CHAR) #apply padding

    return re.findall("..","".join(charlist))


def find_index(grid, char):
    for y in range(0,GRID_SIZE):
        for x in range (0,GRID_SIZE):
            if grid[x][y] == char:
                return (x,y)
    raise Exception("Runtime error, couldn't find index in grid")



def generate_playfair_key(basekey):
    basekey = basekey.replace("i","j")
    basekey = "".join(OrderedDict.fromkeys(basekey))

    global alphabet
    restkey = list(alphabet)

    for char in basekey:
        restkey.remove(char)
    return basekey+"".join(restkey)



def build_grid(key):
    #build grid
    grid = [[None for n in range(GRID_SIZE)] for m in range(GRID_SIZE)]

    for y in range(0,GRID_SIZE):
        for x in range(0,GRID_SIZE):
            grid[x][GRID_SIZE-1-y] = key[GRID_SIZE*y+x]
    return grid


def print_grid(grid):
    for y in range(0,GRID_SIZE):
        for x in range (0,GRID_SIZE):
            print(grid[x][4-y]+" ",end="")
        print()