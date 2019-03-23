import esper
import numpy as np
import tcod as libtcod

from processors.ai_input import AiInputProcessor
from processors.dijkstra import DijkstraProcessor
from processors.render import RenderProcessor

class DebugProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.mouse = None
    
    def process(self):
        self.world.get_processor(RenderProcessor).debug_mode = True
        dijkstra_map = self.world.get_processor(DijkstraProcessor).dijkstra_map
        console = self.world.get_processor(RenderProcessor).console
        
        for (x, y), value in np.ndenumerate(dijkstra_map):
            if value == 999:
                console.print(x, y, '#', libtcod.pink)
            else:
                console.print(x, y, baseN(value, 35), libtcod.pink)

        if self.mouse:
            _coordinate = (self.mouse.cx, self.mouse.cy)
            _value = dijkstra_map[self.mouse.cx, self.mouse.cy]
            console.print(0, 0, str(_coordinate), libtcod.white, bg_blend=libtcod.BKGND_NONE)
            console.print(0, 1, str(_value), libtcod.white, bg_blend=libtcod.BKGND_NONE)

        console.blit(console)
        libtcod.console_flush()
    
    def kill(self):
        self.world.get_processor(RenderProcessor).debug_mode = False

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])