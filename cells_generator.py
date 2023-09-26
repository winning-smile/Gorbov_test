import numpy as np


def create_cell_matrix():
    """Создание случайно матрицы 7х7"""
    matrix = []
    for i in range(1, 26):
        matrix.append(i)

    for i in range(26, 50):
        matrix.append(i)

    np.random.shuffle(matrix)
    return matrix


def distance(x, y, x0, y0):
    """Вычисление расстояние между двумя элементами матрицы"""
    return np.sqrt((x-x0)**2 + (y-y0)**2)


def cell_matrix_distance(matrix):
    """Подсчёт среднего-элементного и полного расстояние для чёрных и красных полей"""
    red = 0
    black = 0

    for i in range(1, 24):
        xy = matrix.index(i)
        xy0 = matrix.index(i+1)
        black += distance(xy//7, xy % 7, xy0//7, xy0 % 7)

    for i in range(25, 49):
        xy = matrix.index(i)
        xy0 = matrix.index(i+1)
        red += distance(xy//7, xy % 7, xy0//7, xy0 % 7)

    avg_red = red/24
    avg_black = black/25

    return black, avg_black, red, avg_red


def create_normalize_matrix():
    """Создание случайной матрицы с ограниченными настройками средне-элементного и полного расстояния"""
    matrix = create_cell_matrix()
    b, avgb, r, avgr = cell_matrix_distance(matrix)
    while (3 > avgb > 4 or 3 > avgr > 4) or ((75 > b or b > 80) or (75 > r or r > 80)):
        matrix = create_cell_matrix()
        b, avgb, r, avgr = cell_matrix_distance(matrix)

    return matrix
