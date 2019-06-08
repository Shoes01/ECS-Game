import esper
import tcod as libtcod

from _data import DoubleLineBox, UI_COLORS, COLOR_THEME
from processors.sub.character_sheet import render_character_sheet
from processors.sub.entities import render_entities
from processors.sub.message_log import render_message_log
from processors.sub.popup_menu import render_popup_menu
from processors.sub.soul_sheet import render_soul_sheet
from processors.sub.stats import render_stats
from processors.sub.tooltips import render_tooltips
from queue import Queue

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.item = None
        self.queue = Queue()
        self.queue.put({'redraw': True})
    
    def process(self):
        self.render_border()
        
        _recompute_fov = False
        _redraw = False

        while not self.queue.empty():
            event = self.queue.get()

            if event.get('recompute_fov'):
                _recompute_fov = True
            elif event.get('redraw'):
                _redraw = True
            elif event.get('item'):
                self.item = event['item']
            elif event.get('item') is False:
                self.item = None

        if not _redraw:
            return 0

        # Draw pretty much all game elements.
        render_stats(self.world)
        render_entities(self.world, _recompute_fov)
        render_popup_menu(self.world)
        render_message_log(self.world, self.item)
        render_tooltips(self.world)
        render_character_sheet(self.world)
        render_soul_sheet(self.world)

        # Draw the gameover overlay.
        if self.world.state == 'GameOver':
            libtcod.console_set_color_control(libtcod.COLCTRL_1, COLOR_THEME['BrightRed'], COLOR_THEME['Red'])
            self.world.consoles['map'][0].print(3, 3, 'You have %cDIED%c! Press ESC to return to the Main Menu.' % (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP), UI_COLORS['text_mainmenu'], bg_blend=libtcod.BKGND_NONE)
        
        # Draw the main menu.
        elif self.world.state == 'MainMenu':
            _string = 'Welcome to the Main Menu.\n\nPress ENTER to begin.\nPress L to load the last save.\n\nPress ESC to quit.'
            self.world.consoles['map'][0].print(3, 3, _string, UI_COLORS['text_mainmenu'])

        # Draw the victory screen
        elif self.world.state == 'VictoryScreen':
            _string = 'You have won! Press ESC to return to the Main Menu.'
            self.world.consoles['map'][0].print(3, 3, _string, UI_COLORS['text_mainmenu'])

        # Blit the consoles.
        for key, value in self.world.consoles.items():
            # key: console name
            # value: console, x, y, w, h
            if key == 'con': continue
            value[0].blit(dest=self.world.consoles['con'][0], dest_x=value[1], dest_y=value[2], width=value[3], height=value[4])

        libtcod.console_flush()

        # Clear the consoles.
        for key, value in self.world.consoles.items():
            value[0].clear()

    def render_border(self):
        if self.world.state == 'MainMenu':
            return 0

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