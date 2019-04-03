import esper
import numpy as np
import tcod as libtcod
import textwrap #DEBUGGING

from components.actor.actor import ActorComponent
from components.corpse import CorpseComponent
from components.game.debug import DebugComponent
from components.game.state import StateComponent
from components.item.equipped import EquippedComponent
from components.item.item import ItemComponent
from components.position import PositionComponent
from components.tile import TileComponent
from components.render import RenderComponent
from processors.sub.entities import render_entities
from processors.sub.message_log import render_message_log
from processors.sub.stats import render_stats

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._consoles = {}
    
    def process(self):
        game_state = self.world.component_for_entity(1, StateComponent).state
        ### TODO: Should all these "processes" be renamed to "render_x"? maybe :)
        # Processing Game state
        if game_state == 'Game' or game_state == 'GameOver':
            self.print_border()
            render_message_log(self._consoles['log'], self.world)
            render_stats(self._consoles['stats'], self.world)
            render_entities(self._consoles['map'], self.world)
        # process MainMenu state
        # process GameOver state

        con_obj = self._consoles['con'] # type: (console, x, y, w, h)
        eqp_obj = self._consoles['stats']
        log_obj = self._consoles['log']
        map_obj = self._consoles['map']

        # The DebugProcessor will print its own stuff.
        if self.world.has_component(1, DebugComponent):
            return 0
            
        if game_state == 'MainMenu':
            map_obj[0].print(3, 3, 'Welcome to the Main Menu.\nPress any key to begin.\n', libtcod.grey)

        if game_state == 'GameOver':
            libtcod.console_set_color_control(libtcod.COLCTRL_1, libtcod.red, libtcod.light_red)
            map_obj[0].print(3, 3, 'You have %cDIED%c! Press ESC to return to the Main Menu.' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP), libtcod.grey, bg_blend=libtcod.BKGND_NONE)            
        
        eqp_obj[0].blit(dest=con_obj[0], dest_x=eqp_obj[1], dest_y=eqp_obj[2], width=eqp_obj[3], height=eqp_obj[4])
        log_obj[0].blit(dest=con_obj[0], dest_x=log_obj[1], dest_y=log_obj[2], width=log_obj[3], height=log_obj[4])
        map_obj[0].blit(dest=con_obj[0], dest_x=map_obj[1], dest_y=map_obj[2], width=map_obj[3], height=map_obj[4])
        libtcod.console_flush()
        
        con_obj[0].clear()
        eqp_obj[0].clear()
        log_obj[0].clear()
        map_obj[0].clear()        
    
    def print_border(self):
        con_obj = self._consoles['con'] # type: (console, x, y, w, h)
        eqp_obj = self._consoles['stats']
        log_obj = self._consoles['log']
        map_obj = self._consoles['map']
        
        for x in range(con_obj[1], con_obj[3]):
            con_obj[0].print(x, con_obj[2], '#', libtcod.dark_grey)
            con_obj[0].print(x, map_obj[2] + map_obj[4], '#', libtcod.dark_grey)
            con_obj[0].print(x, con_obj[2] + con_obj[4] - 1, '#', libtcod.dark_grey)
        
        for y in range(con_obj[2], con_obj[4]):
            con_obj[0].print(con_obj[1], y, '#', libtcod.dark_grey)
            con_obj[0].print(con_obj[1] + con_obj[3] - 1, y, '#', libtcod.dark_grey)
            if y >= eqp_obj[2]:
                con_obj[0].print(eqp_obj[1] + eqp_obj[3], y, '#', libtcod.dark_grey)