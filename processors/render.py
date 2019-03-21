import esper
import numpy as np
import tcod as libtcod

from components.actor import Actor
from components.position import Position
from components.render import Render
from components.tile import Tile

class RenderProcessor(esper.Processor):
    def __init__(self, console):
        super().__init__()
        self.console = console
    
    def process(self):
        # Prepare the console.
        self.console.clear(bg=libtcod.black, fg=libtcod.white)

        # Print walls and stuff.
        for ent, (pos, ren, tile) in self.world.get_components(Position, Render, Tile):
            
            if ren.visible:
                self.console.print(pos.x, pos.y, ren.char, ren.color)
            
            elif ren.explored:
                self.console.print(pos.x, pos.y, ren.char, ren.explored_color)            

        # Print entities to the console.
        for ent, (actor, pos, ren) in self.world.get_components(Actor, Position, Render):
            if ren.visible:
                self.console.print(pos.x, pos.y, ren.char, ren.color)
        
        # Blit console.
        self.console.blit(self.console)

        # Flush console.
        libtcod.console_flush()