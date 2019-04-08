import esper
import numpy as np
import tcod as libtcod

from components.game.debug import DebugComponent
from components.game.state import StateComponent
from components.game.map import MapComponent
from components.game.redraw import RedrawComponent

class DebugProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._consoles = {}
        self._input = (None, None)
    
    def process(self):
        if self.world.has_component(1, DebugComponent) and self.world.component_for_entity(1, StateComponent).state == 'Game':
            dijkstra_map = self.world.component_for_entity(1, MapComponent).dijkstra_map
            key, mouse = self._input
            key_char = None
            con_obj = self._consoles['con'] # type: (console, x, y, w, h)
            map_obj = self._consoles['map']
            log_obj = self._consoles['log']

            # Prepare input.
            try:
                key_char = chr(key.sym)
            except:
                key_char = None

            # Show dijkstra map, but only when the map needs to be redraw.
            if self.world.component_for_entity(1, RedrawComponent).redraw is True:
                self.world.component_for_entity(1, RedrawComponent).redraw = False
                for (x, y), value in np.ndenumerate(dijkstra_map):
                    if value == 999:
                        map_obj[0].print(x, y, '#', libtcod.pink)
                    else:
                        map_obj[0].print(x, y, baseN(value, 35), libtcod.pink)
                
            # Display mouse information.
            if mouse:
                m_x, m_y = mouse.tile
                _string = 'Console coordinate: {:>8}'.format(str((m_x, m_y)))
                con_obj[0].print(log_obj[1], log_obj[2], _string, libtcod.white, bg_blend=libtcod.BKGND_NONE)
                
                if map_obj[1] <= m_x <= map_obj[3] - 1 and map_obj[2] <= m_y <= map_obj[4] - 1:
                    _string = 'Map coordinate: {:>8}'.format(str((m_x - 1, m_y - 1)))
                    con_obj[0].print(log_obj[1], log_obj[2] + 1, _string, libtcod.white, bg_blend=libtcod.BKGND_NONE)
                    _value = dijkstra_map[m_x, m_y]
                    _string = 'Dijkstra value: {:3d}'.format(_value)
                    con_obj[0].print(log_obj[1], log_obj[2] + 2, _string, libtcod.white, bg_blend=libtcod.BKGND_NONE)
                else:
                    _string = '{:>25}'.format(' ')
                    con_obj[0].print(log_obj[1], log_obj[2] + 1, _string, libtcod.white, bg_blend=libtcod.BKGND_NONE)
                    con_obj[0].print(log_obj[1], log_obj[2] + 2, _string, libtcod.white, bg_blend=libtcod.BKGND_NONE)

            # Display last key pressed. TODO: This fails to work, because the InputProcessor pops the event before the debugger gets to read it.
            if key:
                _string = 'Last key pressed: {:>4}'.format(key.scancode)
                if key_char:
                    _string += ' (' + key_char + ')'
                else:
                    _string += ' ( )'
                con_obj[0].print(log_obj[1], log_obj[2] + 3, _string, libtcod.white, bg_blend=libtcod.BKGND_NONE)

            # Send to console.
            map_obj[0].blit(dest=con_obj[0], dest_x=map_obj[1], dest_y=map_obj[2], width=map_obj[3], height=map_obj[4])
            libtcod.console_flush()

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])