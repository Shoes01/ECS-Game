import esper
import tcod as libtcod

from components.action import ActionComponent
from components.game.event import EventComponent
from components.game.state import StateComponent
from components.player import PlayerComponent
from components.turn import TurnComponent

class InputProcessor(esper.Processor):
    def __init__(self, key=None):
        super().__init__()
        self.key = key
    
    def process(self):
        event_component = self.world.component_for_entity(1, EventComponent)
        game_state_component = self.world.component_for_entity(1, StateComponent) # 1 is game entity

        key = self.key
        key_char = chr(key.c)
        action = None

        if game_state_component.state == 'MainMenu':
            if key.vk == libtcod.KEY_ESCAPE:
                event_component.event = 'Exit'
            elif key.pressed:
                event_component.event = 'New_map'

        elif game_state_component.state == 'Game':
            if key.vk == libtcod.KEY_ESCAPE:
                event_component.event = 'Exit'
            if key.vk == libtcod.KEY_UP or key_char == 'k' or key.vk == libtcod.KEY_KP8:
                action = {'move': (0, -1)}
            elif key.vk == libtcod.KEY_DOWN or key_char == 'j' or key.vk == libtcod.KEY_KP2:
                action = {'move': (0, 1)}
            elif key.vk == libtcod.KEY_LEFT or key_char == 'h' or key.vk == libtcod.KEY_KP4:
                action = {'move': (-1, 0)}
            elif key.vk == libtcod.KEY_RIGHT or key_char == 'l' or key.vk == libtcod.KEY_KP6:
                action = {'move': (1, 0)}
            elif key_char == 'y' or key.vk == libtcod.KEY_KP7:
                action = {'move': (-1, -1)}
            elif key_char == 'u' or key.vk == libtcod.KEY_KP9:
                action = {'move': (1, -1)}
            elif key_char == 'b' or key.vk == libtcod.KEY_KP1:
                action = {'move': (-1, 1)}
            elif key_char == 'n' or key.vk == libtcod.KEY_KP3:
                action = {'move': (1, 1)}
            elif key_char == '.' or key.vk == libtcod.KEY_KP5:
                action = {'wait': True}
        
        # Attach action component to player entity.
        if action:
            self.world.add_component(2, ActionComponent(value=action)) # 2 is player entity
            
        self.key = None