import esper
import numpy as np
import tcod as libtcod

from components.position import Position
from components.render import Render

class RenderProcessor(esper.Processor):
    def __init__(self, console, tiles):
        super().__init__()
        self.console = console
        self.tiles = tiles
    
    def process(self):
        # Prepare the console.
        self.console.clear(bg=libtcod.black, fg=libtcod.white)

        # Print walls and stuff.
        for (x, y), (blocks_path) in np.ndenumerate(self.tiles):
            if blocks_path:
                self.console.print(x, y, '#', libtcod.white)

        # Print entities to the console.
        for ent, (pos, ren) in self.world.get_components(Position, Render):
            self.console.print(pos.x, pos.y, ren.char, ren.color)
        
        # Blit console.
        self.console.blit(self.console)

        # Flush console.
        libtcod.console_flush()