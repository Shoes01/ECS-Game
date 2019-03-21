import esper
import numpy as np
import tcod as libtcod

from components.actor import Actor
from components.position import Position
from components.render import Render
from components.tile import Tile

class RenderProcessor(esper.Processor):
    def __init__(self, console, fov_map):
        super().__init__()
        self.console = console
        self.fov_map = fov_map
    
    def process(self):
        # Prepare the console.
        self.console.clear(bg=libtcod.black, fg=libtcod.white)

        # Print walls and stuff.
        for ent, (pos, ren, tile) in self.world.get_components(Position, Render, Tile):
            visible = self.fov_map.fov[pos.x, pos.y]

            if visible:
                tile.explored = True
                self.console.print(pos.x, pos.y, ren.char, ren.color)
            
            elif tile.explored:
                self.console.print(pos.x, pos.y, ren.char, ren.explored_color)            

        # Print entities to the console.
        for ent, (actor, pos, ren) in self.world.get_components(Actor, Position, Render):
            self.console.print(pos.x, pos.y, ren.char, ren.color)
        
        # Blit console.
        self.console.blit(self.console)

        # Flush console.
        libtcod.console_flush()