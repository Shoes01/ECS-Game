import numpy as np
import tcod as libtcod

class Map():
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.fov_map = libtcod.map.Map(self.width, self.height, order='F')
        self.tiles = self.initialize_map()

    def initialize_map(self):
        tiles = np.zeros([self.width, self.height], dtype=[('blocks_path', bool), ('blocks_sight', bool), ('explored', bool)], order='F')
        return tiles

    def initialize_fov(self):
        fov_map = libtcod.map.Map(self.width, self.height, order='F')

        fov_map.walkable[...] = ~self.tiles['blocks_path']
        fov_map.transparent[...] = ~self.tiles['blocks_sight']
        
        return fov_map

    def make_debug_map(self):
        pass
    
