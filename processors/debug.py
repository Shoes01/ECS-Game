import esper
import numpy as np
import tcod as libtcod

from components.game.debug import DebugComponent
from components.game.map import MapComponent

class DebugProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.mouse = None
        self.console = None
    
    def process(self):
        if self.world.has_component(1, DebugComponent):
            dijkstra_map = self.world.component_for_entity(1, MapComponent).dijkstra_map
            console = self.console
            
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

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])