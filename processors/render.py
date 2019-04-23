import esper
import tcod as libtcod

from _data import DoubleLineBox, UI_COLORS, COLOR_THEME
from processors.sub.entities import render_entities
from processors.sub.message_log import render_message_log
from processors.sub.popup_menu import render_popup_menu
from processors.sub.stats import render_stats
from processors.sub.tooltips import render_tooltips

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        game_state = self.world.state
        
        # Draw the border while Debug mode is active.
        if game_state == 'Game' and (self.world.redraw is False or self.world.debug_mode):
            self.render_border()
            return 0
        else:
            self.world.redraw = False

        con_obj = self.world.consoles['con'] # type: (console, x, y, w, h)
        eqp_obj = self.world.consoles['stats']
        log_obj = self.world.consoles['log']
        map_obj = self.world.consoles['map']

        # Draw the main menu.
        if game_state == 'MainMenu':
            _string = 'Welcome to the Main Menu.\n\nPress ENTER to begin.\nPress L to load the last save.\n\nPress ESC to quit.'
            map_obj[0].print(3, 3, _string, UI_COLORS['text_mainmenu'])

        # Draw the victory screen
        if game_state == 'VictoryScreen':
            _string = 'You have won! Press ESC to return to the Main Menu.'
            map_obj[0].print(3, 3, _string, UI_COLORS['text_mainmenu'])

        # Draw the game.
        if game_state == 'Game' or game_state == 'GameOver' or game_state == 'Look' or game_state == 'PopupMenu' or game_state == 'ViewLog' or game_state == 'SkillTargeting':
            self.render_border()
            render_stats(self.world.consoles['stats'], self.world)
            render_entities(self.world.consoles['map'], self.world)
            render_popup_menu(self.world.consoles['map'], self.world)
            render_message_log(self.world.consoles['log'], self.world)
            render_tooltips(self.world.consoles['map'], self.world)

        # Draw the gameover overlay.
        if game_state == 'GameOver':
            libtcod.console_set_color_control(libtcod.COLCTRL_1, COLOR_THEME['BrightRed'], COLOR_THEME['Red'])
            map_obj[0].print(3, 3, 'You have %cDIED%c! Press ESC to return to the Main Menu.' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP), UI_COLORS['text_mainmenu'], bg_blend=libtcod.BKGND_NONE)
        
        # Draw the message log overlay.
        if game_state == 'ViewLog':
            map_obj[0].clear()
            log_obj[0].clear()
            render_message_log(self.world.consoles['map'], self.world)

        eqp_obj[0].blit(dest=con_obj[0], dest_x=eqp_obj[1], dest_y=eqp_obj[2], width=eqp_obj[3], height=eqp_obj[4])
        log_obj[0].blit(dest=con_obj[0], dest_x=log_obj[1], dest_y=log_obj[2], width=log_obj[3], height=log_obj[4])
        map_obj[0].blit(dest=con_obj[0], dest_x=map_obj[1], dest_y=map_obj[2], width=map_obj[3], height=map_obj[4])
        
        libtcod.console_flush()
        
        con_obj[0].clear()
        eqp_obj[0].clear()
        log_obj[0].clear()
        map_obj[0].clear()
    
    def render_border(self):
        con_obj = self.world.consoles['con'] # type: (console, x, y, w, h)
        eqp_obj = self.world.consoles['stats']
        map_obj = self.world.consoles['map']

        box = DoubleLineBox()
        
        for x in range(con_obj[1], con_obj[3]):
            con_obj[0].print(x, con_obj[2], box.horizontal, UI_COLORS['border_main'])
            con_obj[0].print(x, map_obj[2] + map_obj[4], box.horizontal, UI_COLORS['border_main'])
            con_obj[0].print(x, con_obj[2] + con_obj[4] - 1, box.horizontal, UI_COLORS['border_main'])
        
        for y in range(con_obj[2], con_obj[4]):
            con_obj[0].print(con_obj[1], y, box.vertical, UI_COLORS['border_main'])
            con_obj[0].print(con_obj[1] + con_obj[3] - 1, y, box.vertical, UI_COLORS['border_main'])
            if y >= eqp_obj[2]:
                con_obj[0].print(eqp_obj[1] + eqp_obj[3], y, box.vertical, UI_COLORS['border_main'])
        
        con_obj[0].print(con_obj[1], con_obj[2], box.top_left, UI_COLORS['border_main'])
        con_obj[0].print(con_obj[1] + con_obj[3] - 1, con_obj[2], box.top_right, UI_COLORS['border_main'])
        con_obj[0].print(con_obj[1] + con_obj[3] - 1, con_obj[2] + con_obj[4] - 1, box.bottom_right, UI_COLORS['border_main'])
        con_obj[0].print(con_obj[1], con_obj[2] + con_obj[4] - 1, box.bottom_left, UI_COLORS['border_main'])

        con_obj[0].print(eqp_obj[1] - 1, eqp_obj[2] - 1, box.not_left, UI_COLORS['border_main'])
        con_obj[0].print(eqp_obj[1] + eqp_obj[3], eqp_obj[2] - 1, box.not_up, UI_COLORS['border_main'])
        con_obj[0].print(eqp_obj[1] + eqp_obj[3], eqp_obj[2] + eqp_obj[4], box.not_down, UI_COLORS['border_main'])
        con_obj[0].print(map_obj[1] + map_obj[3], map_obj[2] + map_obj[4], box.not_right, UI_COLORS['border_main'])