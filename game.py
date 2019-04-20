import world

class GameWorld(world.CustomWorld):
    def __init__(self):
        super().__init__()
        self.debug_mode = False