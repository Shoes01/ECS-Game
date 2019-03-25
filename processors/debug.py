import esper
import numpy as np
import tcod as libtcod

from components.game.debug import DebugComponent
from components.game.map import MapComponent

class DebugProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._console = None
        self._key = None
        self._mouse = None
    
    def process(self):
        if self.world.has_component(1, DebugComponent):
            dijkstra_map = self.world.component_for_entity(1, MapComponent).dijkstra_map
            console = self._console
            
            for (x, y), value in np.ndenumerate(dijkstra_map):
                if value == 999:
                    console.print(x, y, '#', libtcod.pink)
                else:
                    console.print(x, y, baseN(value, 35), libtcod.pink)

            if self._mouse:
                _coordinate = (self._mouse.cx, self._mouse.cy)
                _value = dijkstra_map[self._mouse.cx, self._mouse.cy]
                console.print(0, 0, str(_coordinate), libtcod.white, bg_blend=libtcod.BKGND_NONE)
                console.print(0, 1, str(_value), libtcod.white, bg_blend=libtcod.BKGND_NONE)

            last_key_char = None
            if self._key and self._key.pressed:
                last_key_char = self._key.text
            if last_key_char:
                console.print(0, 2, last_key_char, libtcod.white, bg_blend=libtcod.BKGND_NONE)

            console.blit(console)
            libtcod.console_flush()

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])