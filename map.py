import numpy as np
import tcod as libtcod

class Map():
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.tiles = np.zeros([self.width, self.height], dtype=int, order='F')