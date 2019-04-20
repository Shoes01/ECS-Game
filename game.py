import world

class GameWorld(world.CustomWorld):
    def __init__(self):
        super().__init__()
        self.debug_mode = False
        self.create_dijkstra_map = False
        self.generate_map = False
        self.view_log = False