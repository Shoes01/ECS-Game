import esper
import tcod as libtcod

from fabricator import fabricate_entity

class InitialProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        if not self.world._entities:
            # Create game meta-entity. It is ID 1.
            fabricate_entity('game', self.world)

            # Create the player entity. It is ID 2.
            fabricate_entity('player', self.world)