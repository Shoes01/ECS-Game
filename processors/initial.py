import esper
import tcod as libtcod

class InitialProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        if not self.world._entities:
            # Create the player entity. It is ID 1.
            self.world.create_entity('player')