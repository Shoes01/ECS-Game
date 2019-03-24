class MapComponent():
    def __init__(self, height, width):
        self.height = height
        self.dijkstra_map = None
        self.directory = None
        self.fov_map = None
        self.tiles = None
        self.width = width