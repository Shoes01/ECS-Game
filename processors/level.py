import esper
import numpy as np
import tcod as libtcod

from components.game.level import LevelComponent
from components.position import Position
from components.render import Render
from components.tile import Tile
from processors.prerender import PrerenderProcessor

class LevelProcessor(esper.Processor):
    def __init__(self, height, tiles, width):
        super().__init__()
        self.height = height
        self.tiles = tiles
        self.width = width

    def process(self):
        if self.world.has_component(1, LevelComponent):
            # Create level.
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
            
            # Create fov map.
            fov_map = libtcod.map.Map(self.width, self.height, order='F')
            for ent, (pos, tile) in self.world.get_components(Position, Tile):
                fov_map.walkable[pos.x, pos.y] = not tile.blocks_path
                fov_map.transparent[pos.x, pos.y] = not tile.blocks_sight
            self.world.get_processor(PrerenderProcessor).fov_map = fov_map