from constants import *


def check_boundary(row, col):
    """
    returns neighbors of the given cell
    """
    neighbors = []
    if row < HEIGHT-1:
        neighbors.append([row+1], [col])
    if row > 0:
        neighbors.append([row-1], [col])
    if col < WIDTH-1:
        neighbors.append([row], [col+1])
    if col > 0:
        neighbors.append([row], [col-1])
