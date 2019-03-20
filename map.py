import numpy as np

class Map():
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.tiles = self.initialize_map()

    def initialize_map(self):
        tiles = np.zeros([self.width, self.height], dtype=[('blocks_sight', bool), ('blocks_path', bool)], order='F')        
        return tiles

    def make_debug_map(self):
        self.tiles[17, 17] = True, True