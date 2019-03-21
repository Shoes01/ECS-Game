import esper
import numpy as np
import tcod as libtcod

from components.game.level import LevelComponent
from components.position import Position
from components.render import Render
from components.tile import Tile

class LevelProcessor(esper.Processor):
    def __init__(self, tiles):
        super().__init__()
        self.tiles = tiles

    def process(self):
        if self.world.has_component(1, LevelComponent):
            # Create floor.
            for (x, y), _ in np.ndenumerate(self.tiles):
                if x == 17 and y == 17:
                    wall = self.world.create_entity()
                    self.world.add_component(wall, Position(x=x, y=y))
                    self.world.add_component(wall, Render(char='#', color=libtcod.white, explored_color=libtcod.darkest_grey))
                    self.world.add_component(wall, Tile())
                else:
                    floor = self.world.create_entity()
                    self.world.add_component(floor, Position(x=x, y=y))
                    self.world.add_component(floor, Render(char='.', color=libtcod.white, explored_color=libtcod.darkest_grey))
                    self.world.add_component(floor, Tile(False, False))