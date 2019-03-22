import esper
import numpy as np
import tcod as libtcod

from components.game.mapgen import MapgenComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent
from processors.prerender import PrerenderProcessor

class MapgenProcessor(esper.Processor):
    def __init__(self, height, width):
        super().__init__()
        self.height = height        
        self.width = width

        self.tiles = self.tiles = np.zeros([self.width, self.height], dtype=int, order='F')

    def process(self):
        if self.world.has_component(1, MapgenComponent):
            # Create new map.
            self.create_map()
            
            # Create fov map.
            self.create_fov_map()
            
            # Finished. Remove the component.
            self.world.remove_component(1, MapgenComponent)
    
    def create_map(self):
        for (x, y), _ in np.ndenumerate(self.tiles):
            if x == 17 and y == 17:
                wall = self.world.create_entity()
                self.world.add_component(wall, PositionComponent(x=x, y=y))
                self.world.add_component(wall, RenderComponent(char='#', color=libtcod.white, explored_color=libtcod.darkest_grey))
                self.world.add_component(wall, TileComponent())
            else:
                floor = self.world.create_entity()
                self.world.add_component(floor, PositionComponent(x=x, y=y))
                self.world.add_component(floor, RenderComponent(char='.', color=libtcod.white, explored_color=libtcod.darkest_grey))
                self.world.add_component(floor, TileComponent(False, False))

    def create_fov_map(self):
        fov_map = libtcod.map.Map(self.width, self.height, order='F')
        for ent, (pos, tile) in self.world.get_components(PositionComponent, TileComponent):
            fov_map.walkable[pos.x, pos.y] = not tile.blocks_path
            fov_map.transparent[pos.x, pos.y] = not tile.blocks_sight
        self.world.get_processor(PrerenderProcessor).fov_map = fov_map