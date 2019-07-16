class Map():
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.dijkstra_map = None
        self.directory = None
        self.fov_map = None
        self.tiles = None
        self.floor = 0
        