import esper
import tcod as libtcod

from _data import DoubleLineBox, UI_COLORS
from processors.sub.character_sheet import render_character_sheet
from processors.sub.entities import render_entities
from processors.sub.game_over import render_game_over
from processors.sub.main_menu import render_main_menu
from processors.sub.message_log import render_message_log
from processors.sub.popup_menu import render_popup_menu
from processors.sub.skill_display import render_skill_display
from processors.sub.soul_sheet import render_soul_sheet
from processors.sub.stats import render_stats
from processors.sub.tooltips import render_tooltips
from processors.sub.victory import render_victory_screen
from queue import Queue

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.item = None
        self.queue = Queue()
        self.queue.put({'redraw': True})
    
    def process(self):
        _recompute_fov = False
        _redraw = False
        _new_turn = False
        _soul = None
        
        while not self.queue.empty():
            # This queue is different from the Processor queues.
            # Every event is read and remembered, and then all done on the same tick.
            # That's why there is a if/else chain here.
            event = self.queue.get()

            if event.get('item'):
                self.item = event['item']
            elif event.get('item') is False:
                self.item = None
            elif event.get('new_turn'):
                _new_turn = event.get('new_turn')
            elif event.get('recompute_fov'):
                _recompute_fov = event.get('recompute_fov')
            elif event.get('redraw'):
                _redraw = event.get('redraw')
            elif event.get('soul'):
                _soul = event.get('soul')

        if not _redraw:
            return 0

        # Draw the borders.
        self.render_border()

        # Draw each console.
        self.draw_stats(console=self.world.consoles['stats'], state=self.world.state, world=self.world)
        self.draw_log(console=self.world.consoles['log'], item=self.item, new_turn=_new_turn, state=self.world.state, world=self.world)
        self.draw_map(console=self.world.consoles['map'], recompute_fov=_recompute_fov, state=self.world.state, soul=_soul, world=self.world)

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
        

    def draw_stats(self, console, state, world):
        if state != 'MainMenu':
            render_stats(console, world)
    
    def draw_log(self, console, item, new_turn, state, world):
        if state == 'SkillTargeting':
            render_skill_display(console, item, world)
        elif state != 'MainMenu':
            render_message_log(console, new_turn, world)

    def draw_map(self, console, recompute_fov, state, soul, world):
        # Splash screen.
        if state == 'MainMenu':
            render_main_menu(console)
        
        # Main game content.
        if state != 'MainMenu' and state != 'PopupMenu':
            render_entities(console, recompute_fov, world)
            render_tooltips(console, world)
        
        # Various menus.
        if state == 'ViewCharacterSheet':
            render_character_sheet(console, world)
        elif state == 'PopupMenu':
            render_popup_menu(console, world)
        elif state == 'SoulState' and soul:
            render_soul_sheet(console, soul, world)
        elif state == 'GameOver':
            render_game_over(console)
        elif state == 'VictoryScreen':
            render_victory_screen(console)

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