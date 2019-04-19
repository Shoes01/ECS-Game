from _data import map

class MapComponent():
    def __init__(self):
        self.height = map.h
        self.dijkstra_map = None
        self.directory = None
        self.fov_map = None
        self.tiles = None
        self.width = map.w
        self.floor = 0