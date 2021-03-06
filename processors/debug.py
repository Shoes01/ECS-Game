import esper
import numpy as np
import tcod as libtcod

from components.actor.actor import ActorComponent
from components.furniture import FurnitureComponent
from components.item.item import ItemComponent
from components.tile import TileComponent
from fsm import Game
from queue import Queue

class DebugProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        if not (self.world.toggle_debug_mode and self.world.state == Game):
            return 0
        
        dijkstra_map = self.world.map.dijkstra_map
        key = self.world.key
        key_char = None
        mouse_pos = self.world.mouse_pos
        _redraw = False

        while not self.queue.empty():
            event = self.queue.get()
            _redraw = event.get('redraw')
        
        con_obj = self.world.consoles['con'] # type: (console, x, y, w, h)
        map_obj = self.world.consoles['map']
        log_obj = self.world.consoles['log']

        # Prepare input.
        try:
            key_char = chr(key.sym)
        except:
            key_char = None

        # Show dijkstra map, but only when the map needs to be redraw.
        if _redraw:
            # TODO: Fix the positioning of the dijkstra values
            for (x, y), value in np.ndenumerate(dijkstra_map):
                if value == 999:
                    map_obj[0].print(x, y, '#', libtcod.pink)
                else:
                    map_obj[0].print(x, y, baseN(value, 35), libtcod.pink)
            
        # Display mouse information.
        if mouse_pos and False:
            # TODO: when this works, the game crashes
            m_x, m_y = mouse_pos
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

        # Split the entities into groups.
        _actors = {}
        _items = {}
        _furniture = {}
        _tiles = {}
        _other = {}
        for ent, comps in self.world._entities.items():
            if self.world.has_component(ent, FurnitureComponent):
                _furniture[ent] = comps
            elif self.world.has_component(ent, ActorComponent):
                _actors[ent] = comps
            elif self.world.has_component(ent, ItemComponent):
                _items[ent] = comps
            elif self.world.has_component(ent, TileComponent):
                _tiles[ent] = comps
            else:
                _other[ent] = comps

        # Send to console.
        map_obj[0].blit(dest=con_obj[0], dest_x=map_obj[1], dest_y=map_obj[2], width=map_obj[3], height=map_obj[4])
        libtcod.console_flush()

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])