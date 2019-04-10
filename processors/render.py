import esper
import tcod as libtcod

from _data import DoubleLineBox
from components.game.debug import DebugComponent
from components.game.redraw import RedrawComponent
from components.game.state import StateComponent
from processors.sub.entities import render_entities
from processors.sub.message_log import render_message_log
from processors.sub.popup_menu import render_popup_menu
from processors.sub.stats import render_stats

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._consoles = {}
    
    def process(self):
        game_state = self.world.component_for_entity(1, StateComponent).state
        
        if game_state == 'Game' and (self.world.component_for_entity(1, RedrawComponent).redraw is False or self.world.has_component(1, DebugComponent)):
            self.render_border()
            return 0
        else:
            self.world.component_for_entity(1, RedrawComponent).redraw = False

        con_obj = self._consoles['con'] # type: (console, x, y, w, h)
        eqp_obj = self._consoles['stats']
        log_obj = self._consoles['log']
        map_obj = self._consoles['map']



        if game_state == 'Game' or game_state == 'GameOver' or game_state == 'PopupMenu':
            self.render_border()
            render_message_log(self._consoles['log'], self.world)
            render_stats(self._consoles['stats'], self.world)
            render_entities(self._consoles['map'], self.world)
            render_popup_menu(self._consoles['map'], self.world)
        
        if game_state == 'MainMenu':
            _string = 'Welcome to the Main Menu.\n\nPress ENTER to begin.\nPress L to load the last save.\n\nPress ESC to quit.'
            map_obj[0].print(3, 3, _string, libtcod.grey)

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
    
    def render_border(self):
        con_obj = self._consoles['con'] # type: (console, x, y, w, h)
        eqp_obj = self._consoles['stats']
        map_obj = self._consoles['map']

        box = DoubleLineBox()
        
        for x in range(con_obj[1], con_obj[3]):
            con_obj[0].print(x, con_obj[2], box.horizontal, libtcod.dark_grey)
            con_obj[0].print(x, map_obj[2] + map_obj[4], box.horizontal, libtcod.dark_grey)
            con_obj[0].print(x, con_obj[2] + con_obj[4] - 1, box.horizontal, libtcod.dark_grey)
        
        for y in range(con_obj[2], con_obj[4]):
            con_obj[0].print(con_obj[1], y, box.vertical, libtcod.dark_grey)
            con_obj[0].print(con_obj[1] + con_obj[3] - 1, y, box.vertical, libtcod.dark_grey)
            if y >= eqp_obj[2]:
                con_obj[0].print(eqp_obj[1] + eqp_obj[3], y, box.vertical, libtcod.dark_grey)
        
        con_obj[0].print(con_obj[1], con_obj[2], box.top_left, libtcod.dark_grey)
        con_obj[0].print(con_obj[1] + con_obj[3] - 1, con_obj[2], box.top_right, libtcod.dark_grey)
        con_obj[0].print(con_obj[1] + con_obj[3] - 1, con_obj[2] + con_obj[4] - 1, box.bottom_right, libtcod.dark_grey)
        con_obj[0].print(con_obj[1], con_obj[2] + con_obj[4] - 1, box.bottom_left, libtcod.dark_grey)

        con_obj[0].print(eqp_obj[1] - 1, eqp_obj[2] - 1, box.not_left, libtcod.dark_grey)
        con_obj[0].print(eqp_obj[1] + eqp_obj[3], eqp_obj[2] - 1, box.not_up, libtcod.dark_grey)
        con_obj[0].print(eqp_obj[1] + eqp_obj[3], eqp_obj[2] + eqp_obj[4], box.not_down, libtcod.dark_grey)
        con_obj[0].print(map_obj[1] + map_obj[3], map_obj[2] + map_obj[4], box.not_right, libtcod.dark_grey)