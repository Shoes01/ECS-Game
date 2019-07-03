from _data import map, MULTIPLIER

class Map():
    def __init__(self):
        self.height = map.h // MULTIPLIER
        self.dijkstra_map = None
        self.directory = None
        self.fov_map = None
        self.tiles = None
        self.width = map.w // MULTIPLIER # TODO: When a camera system is in place, this value can be arbitarily set.
        self.floor = 0
        