import numpy as np


def create_cell_matrix():
    matrix = []
    for i in range(1, 26):
        matrix.append(i)

    for i in range(26, 50):
        matrix.append(i)

    np.random.shuffle(matrix)
    return matrix


def distance(x, y, x0, y0):
    return np.sqrt((x-x0)**2 + (y-y0)**2)


def cell_matrix_distance(matrix):
    red = 0
    black = 0

    for i in range(1, 24):
        xy = matrix.index(i)
        xy0 = matrix.index(i+1)
        black += distance(xy//7, xy%7, xy0//7, xy0%7)

    for i in range(25, 49):
        xy = matrix.index(i)
        xy0 = matrix.index(i+1)
        red += distance(xy//7, xy%7, xy0//7, xy0%7)

    avg_red = red/24
    avg_black = black/25

    print(black, avg_black, red, avg_red)
    return black, avg_black, red, avg_red


def create_normalize_matrix():
    matrix = create_cell_matrix()
    b, avgb, r, avgr = cell_matrix_distance(matrix)
    while (3 > avgb > 4 or 3 > avgr > 4) or ((75 > b or b > 80) or (75 > r or r > 80)):
        matrix = create_cell_matrix()
        b, avgb, r, avgr = cell_matrix_distance(matrix)
        print(b, avgb, r, avgr)

    return matrix

