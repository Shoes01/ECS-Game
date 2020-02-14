import esper
import math
import tcod as libtcod
import tcod.event

from components.actor.actor import ActorComponent
from components.actor.energy import EnergyComponent
from components.actor.player import PlayerComponent
from components.position import PositionComponent
from fsm import Game, GameOver, Look, MainMenu, SkillTargeting, SoulState, VictoryScreen, ViewCharacterSheet, ViewLog
from fsm import PopupMenu as PopupMenuState
from processors.consumable import ConsumableProcessor
from processors.debug import DebugProcessor
from processors.descend import DescendProcessor
from processors.drop import DropProcessor
from processors.energy import EnergyProcessor
from processors.event import EventProcessor
from processors.final import FinalProcessor
from processors.inventory import InventoryProcessor
from processors.job import JobProcessor
from processors.mapgen import MapgenProcessor
from processors.movement import MovementProcessor
from processors.new_game import NewGameProcessor
from processors.pickup import PickupProcessor
from processors.removable import RemovableProcessor
from processors.skill import SkillProcessor
from processors.skill_menu import SkillMenuProcessor
from processors.soul import SoulProcessor
from processors.state import StateProcessor
from processors.render import RenderProcessor
from processors.wearable import WearableProcessor

class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        key = None
        key_char = None
        mouse = None
        mouse_click = None
        key_scancode = None

        for event in libtcod.event.get():
            if event.type == 'KEYDOWN':
                key = event
            elif event.type == 'MOUSEMOTION':
                mouse = event
            elif event.type == 'MOUSEBUTTONDOWN':
                mouse_click = event

        if mouse:
            self.world.get_processor(EventProcessor).queue.put({'mouse_pos': (mouse.tile.x, mouse.tile.y)})
            self.world.get_processor(RenderProcessor).queue.put({'redraw': True})

        if key or mouse_click:
            self.world.get_processor(DebugProcessor).queue.put({'redraw': True})
            self.world.get_processor(RenderProcessor).queue.put({'redraw': True})

        try:
            key_char = chr(key.sym)
        except:
            key_char = None

        if key:
            key_scancode = key.scancode

        if key_char == 'd' and key.mod & libtcod.event.KMOD_CTRL:
            self.world.get_processor(EventProcessor).queue.put({'toggle_debug': True})

        if self.world.state == PopupMenuState:
            self.handle_popupmenu_input(key_char, key_scancode)
        elif self.world.state == MainMenu:
            self.handle_mainmenu_input(key_char, key_scancode)
        elif self.world.state == ViewLog:
            self.handle_viewlog_input(key_char, key_scancode)
        elif self.world.state == Look:
            self.handle_look_input(key_char, key_scancode)
        elif self.world.state == GameOver:
            self.handle_gameover_input(key_char, key_scancode)
        elif self.world.state == VictoryScreen:
            self.handle_victoryscreen_input(key_char, key_scancode)
        elif self.world.state == Game:
            self.handle_game_input(key, key_char, key_scancode, mouse_click)
        elif self.world.state == SkillTargeting:
            self.handle_skilltargeting_input(key_char, key_scancode)
        elif self.world.state == ViewCharacterSheet:
            self.handle_viewcharactersheet_input(key_char, key_scancode)
        elif self.world.state == SoulState:
            self.handle_soulstate_input(key_char, key_scancode)
        
    def handle_popupmenu_input(self, key_char, key_scancode):
        menu = self.world.popup_menus[-1]
        
        for choice in menu.contents:
            if key_char == choice.key:
                for result in choice.results:
                    self.world.get_processor(result.processor).queue.put(result.result) 
                
                if menu.auto_close:
                    self.world.get_processor(StateProcessor).queue.put({'exit': True})
        else:
            if menu.include_esc and key_scancode == libtcod.event.SCANCODE_ESCAPE:
                self.world.get_processor(StateProcessor).queue.put({'pop': True})

    def handle_mainmenu_input(self, key_char, key_scancode):
        if key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.running = False
            self.world.get_processor(StateProcessor).queue.put({'exit': True})
        elif key_scancode == libtcod.event.SCANCODE_KP_ENTER or key_scancode == libtcod.event.SCANCODE_RETURN:
            self.world.get_processor(MapgenProcessor).queue.put({'generate_dungeon': True})
            self.world.get_processor(NewGameProcessor).queue.put({'new_game': True})
            self.world.get_processor(StateProcessor).queue.put({'new_game': True})
        elif key_char == 'l':
            self.world.load_game()
            self.world.get_processor(StateProcessor).queue.put({'load_game': True})

    def handle_viewlog_input(self, key_char, key_scancode):
        if key_scancode == libtcod.event.SCANCODE_UP or key_char == 'k' or key_scancode == libtcod.event.SCANCODE_KP_8:
            self.world.get_processor(EventProcessor).queue.put({'scroll': +1})
        elif key_scancode == libtcod.event.SCANCODE_DOWN or key_char == 'j' or key_scancode == libtcod.event.SCANCODE_KP_2:
            self.world.get_processor(EventProcessor).queue.put({'scroll': -1})
        elif key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.get_processor(StateProcessor).queue.put({'exit': True})

    def handle_look_input(self, key_char, key_scancode):
        result = self.generic_move_keys(key_char, key_scancode)
        if result:
            self.world.get_processor(EventProcessor).queue.put(result)
        elif key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.get_processor(StateProcessor).queue.put({'exit': True})

    def handle_gameover_input(self, key_char, key_scancode):
        if key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
            self.world.get_processor(StateProcessor).queue.put({'exit': True})

    def handle_victoryscreen_input(self, key_char, key_scancode):
        if key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.get_processor(FinalProcessor).queue.put({'reset_game': True})
            self.world.get_processor(StateProcessor).queue.put({'exit': True})

    def handle_skilltargeting_input(self, key_char, key_scancode):
        result = self.generic_move_keys(key_char, key_scancode)
        if result:
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_move': result['move']})
        elif key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_clear': True})
        elif key_char == 'q':
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_prepare': 'mainhand'})
        elif key_char == 'w':
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_prepare': 'head'})
        elif key_char == 'e':
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_prepare': 'accessory'})
        elif key_char == 'a':
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_prepare': 'offhand'})
        elif key_char == 's':
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_prepare': 'torso'})
        elif key_char == 'd':
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_prepare': 'feet'})
        elif key_scancode == libtcod.event.SCANCODE_SPACE:
            self.world.get_processor(SkillProcessor).queue.put({'ent': 1, 'skill_confirm': True})

    def handle_game_input(self, key, key_char, key_scancode, mouse_click):
        if key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.get_processor(EventProcessor).queue.put({'open_main_menu': True})
        elif key_char == 'm':
            self.world.get_processor(StateProcessor).queue.put({'view_log': True})
        elif key_char == 'x':
            _pos = self.world.component_for_entity(1, PositionComponent)
            self.world.get_processor(EventProcessor).queue.put({'look': (_pos.x, _pos.y)})
        elif key_char == 'c':
            self.world.get_processor(StateProcessor).queue.put({'view_character_sheet': True})
        
        # These keys can only be read if the player has move priority.
        elif self.world.component_for_entity(1, EnergyComponent).energy == 0:
            # Movement keys.
            result = self.generic_move_keys(key_char, key_scancode, key=key)
            if result:
                self.world.get_processor(MovementProcessor).queue.put(result)
            
            # Other keys.
            elif key_char == 'd' and key.mod & libtcod.event.KMOD_SHIFT:
                self.world.get_processor(DropProcessor).queue.put({'ent': 1})
            elif key_char == 'e' and key.mod & libtcod.event.KMOD_SHIFT:
                self.world.get_processor(ConsumableProcessor).queue.put({'ent': 1})
            elif key_char == 'g':
                self.world.get_processor(PickupProcessor).queue.put({'ent': 1})
            elif key_char == 'i':
                self.world.get_processor(InventoryProcessor).queue.put({'ent': 1})
            elif (key_char == 'w' and key.mod & libtcod.event.KMOD_SHIFT) or key_char == 'r':
                self.world.get_processor(WearableProcessor).queue.put({'ent': 1})
            elif key_char == '>' or key_char == '<':
                self.world.get_processor(DescendProcessor).queue.put({'ent': 1})
            elif key_char == 'j' and key.mod & libtcod.event.KMOD_SHIFT:
                self.world.get_processor(JobProcessor).queue.put({'ent': 1})

            # Skill menu keys.
            elif key_char in ['q', 'w', 'e', 'a', 's', 'd'] and key.mod & libtcod.event.KMOD_SHIFT:
                self.world.get_processor(SkillMenuProcessor).queue.put({'skill_menu': key_char, 'ent': 1})

            # Skill keys. TODO: Convert this to look like above. Use the KEY_TO_SLOTS in SkillProcessor to convert back to slot.
            elif key_char == 'q':
                self.world.get_processor(SkillProcessor).queue.put({'skill_prepare': 'mainhand', 'ent': 1})
            elif key_char == 'w':
                self.world.get_processor(SkillProcessor).queue.put({'skill_prepare': 'head', 'ent': 1})
            elif key_char == 'e':
                self.world.get_processor(SkillProcessor).queue.put({'skill_prepare': 'accessory', 'ent': 1})
            elif key_char == 'a':
                self.world.get_processor(SkillProcessor).queue.put({'skill_prepare': 'offhand', 'ent': 1})
            elif key_char == 's':
                self.world.get_processor(SkillProcessor).queue.put({'skill_prepare': 'torso', 'ent': 1})
            elif key_char == 'd':
                self.world.get_processor(SkillProcessor).queue.put({'skill_prepare': 'feet', 'ent': 1})
            
            # Mouse movement.
            if mouse_click:
                mx, my = mouse_click.tile.x, mouse_click.tile.y
                pos = self.world.component_for_entity(1, PositionComponent)

                dx = mx - pos.x
                dy = my - pos.y
                r = math.sqrt( dx**2 + dy**2)

                _move = round(dx/r), round(dy/r)
                self.world.get_processor(MovementProcessor).queue.put({'move': _move, 'ent': 1})

    def handle_viewcharactersheet_input(self, key_char, key_scancode):
        if key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.get_processor(StateProcessor).queue.put({'exit': True})

    def handle_soulstate_input(self, key_char, key_scancode):
        result = self.generic_move_keys(key_char, key_scancode)
        if key_scancode == libtcod.event.SCANCODE_ESCAPE:
            self.world.get_processor(SoulProcessor).queue.put({'cancel': True})
            self.world.get_processor(StateProcessor).queue.put({'exit': True})
        elif result:
            self.world.get_processor(SoulProcessor).queue.put({'rotate': result['move']})
        elif key_scancode == libtcod.event.SCANCODE_KP_ENTER or key_scancode == libtcod.event.SCANCODE_RETURN:
            self.world.get_processor(SoulProcessor).queue.put({'ent': 1, 'confirm': True})

    def generic_move_keys(self, key_char, key_scancode, key=None):
        result = {}

        if key and key.mod & libtcod.event.KMOD_SHIFT:
            return result
        
        if   key_char == 'k' or key_scancode == libtcod.event.SCANCODE_KP_8 or key_scancode == libtcod.event.SCANCODE_UP:
            result = {'ent': 1, 'move': (0, -1)}
        elif key_char == 'j' or key_scancode == libtcod.event.SCANCODE_KP_2 or key_scancode == libtcod.event.SCANCODE_DOWN:
            result = {'ent': 1, 'move': (0, 1)}
        elif key_char == 'h' or key_scancode == libtcod.event.SCANCODE_KP_4 or key_scancode == libtcod.event.SCANCODE_LEFT:
            result = {'ent': 1, 'move': (-1, 0)}
        elif key_char == 'l' or key_scancode == libtcod.event.SCANCODE_KP_6 or key_scancode == libtcod.event.SCANCODE_RIGHT:
            result = {'ent': 1, 'move': (1, 0)}
        elif key_char == 'y' or key_scancode == libtcod.event.SCANCODE_KP_7:
            result = {'ent': 1, 'move': (-1, -1)}
        elif key_char == 'u' or key_scancode == libtcod.event.SCANCODE_KP_9:
            result = {'ent': 1, 'move': (1, -1)}
        elif key_char == 'b' or key_scancode == libtcod.event.SCANCODE_KP_1:
            result = {'ent': 1, 'move': (-1, 1)}
        elif key_char == 'n' or key_scancode == libtcod.event.SCANCODE_KP_3:
            result = {'ent': 1, 'move': (1, 1)}
        elif key_char == '.' or key_scancode == libtcod.event.SCANCODE_KP_5:
            result = {'ent': 1, 'move': False}
        
        return result