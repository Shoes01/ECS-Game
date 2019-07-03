from _data import map

class Map():
    def __init__(self):
        self.height = map.h // 2
        self.dijkstra_map = None
        self.directory = None
        self.fov_map = None
        self.tiles = None
        self.width = map.w // 2
        self.floor = 0
        