import esper
import numpy as np
import tcod as libtcod

from components.game.debug import DebugComponent
from components.game.map import MapComponent

class DebugProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._consoles = {}
        self._key = None
        self._mouse = None
    
    def process(self):
        if self.world.has_component(1, DebugComponent):
            con_obj = self._consoles['con'] # type: (console, x, y, w, h)
            eqp_obj = self._consoles['stats']
            log_obj = self._consoles['log']
            map_obj = self._consoles['map']

            eqp_obj[0].clear(bg=libtcod.pink, fg=libtcod.white)
            log_obj[0].clear(bg=libtcod.red, fg=libtcod.white)
            map_obj[0].clear(bg=libtcod.green, fg=libtcod.white)

            dijkstra_map = self.world.component_for_entity(1, MapComponent).dijkstra_map
            
            # Show dijkstra map.
            for (x, y), value in np.ndenumerate(dijkstra_map):
                if value == 999:
                    map_obj[0].print(x, y, '#', libtcod.pink)
                else:
                    map_obj[0].print(x, y, baseN(value, 35), libtcod.pink)

            # Display mouse information.
            if self._mouse:
                c, x, y, w, h = map_obj
                
                _coordinate = (self._mouse.cx, self._mouse.cy)
                map_obj[0].print(0, 0, str(_coordinate), libtcod.white, bg_blend=libtcod.BKGND_NONE)
                
                if x <= self._mouse.cx <= w - 1 and y <= self._mouse.cy <= h - 1:
                    _value = dijkstra_map[self._mouse.cx, self._mouse.cy]
                    map_obj[0].print(0, 1, str(_value), libtcod.white, bg_blend=libtcod.BKGND_NONE)

            # Display last key pressed TODO: Fix this.
            last_key_char = None
            if self._key and self._key.pressed:
                last_key_char = self._key.text
            if last_key_char:
                map_obj[0].print(0, 2, last_key_char, libtcod.white, bg_blend=libtcod.BKGND_NONE)

            # Test
            eqp_obj[0].print(0, 0, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', libtcod.white)

            # Send to console.
            eqp_obj[0].blit(dest=con_obj[0], dest_x=eqp_obj[1], dest_y=eqp_obj[2], width=eqp_obj[3], height=eqp_obj[4])
            log_obj[0].blit(dest=con_obj[0], dest_x=log_obj[1], dest_y=log_obj[2], width=log_obj[3], height=log_obj[4])
            map_obj[0].blit(dest=con_obj[0], dest_x=map_obj[1], dest_y=map_obj[2], width=map_obj[3], height=map_obj[4])
            libtcod.console_flush()

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])