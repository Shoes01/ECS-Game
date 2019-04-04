import esper
import tcod as libtcod

from components.actor.action import ActionComponent
from components.actor.player import PlayerComponent
from components.actor.player_input import PlayerInputComponent
from components.game.event import EventComponent
from components.game.popup import PopupComponent
from components.game.state import StateComponent

class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._key = None
        self._mouse = None
    
    def process(self):
        if self.world.has_component(2, PlayerInputComponent):
            event_component = self.world.component_for_entity(1, EventComponent)
            game_state_component = self.world.component_for_entity(1, StateComponent)

            key = self._key
            key_char = chr(key.c)
            action = None

            if key.vk is libtcod.KEY_NONE:
                return 0

            if key_char == 'd' and key.lctrl:
                event_component.event = 'Toggle_debug_mode'

            if game_state_component.state == 'MainMenu':
                if key.vk == libtcod.KEY_ESCAPE:
                    event_component.event = 'Exit'
                elif key.pressed:
                    event_component.event = 'New_map'

            elif game_state_component.state == 'Game':
                if key.vk == libtcod.KEY_ESCAPE:
                    popup_component = PopupComponent(
                        title='Are you sure you want to quit?',
                        choices=[
                            (
                                'Yes',
                                'y',
                                {'event': 'Exit'}
                            ),
                            (
                                'No',
                                'n',
                                {'event': 'Cancel'}
                            )
                        ]
                    )
                    self.world.add_component(1, popup_component)
                    event_component.event = 'PopupMenu'
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
                
                if key_char == 'g':
                    action = {'pick_up': True}
            
            elif game_state_component.state == 'GameOver':
                if key.vk == libtcod.KEY_ESCAPE:
                    event_component.event = 'Exit'

            elif game_state_component.state == 'PopupMenu':
                _popup_comp = self.world.component_for_entity(1, PopupComponent)
                for choice in _popup_comp.choices:
                    title, valid_key, result = choice
                    if key_char == valid_key:
                        if result.get('event'):
                            event_component.event = result['event']
                        if result.get('action'):
                            action = result['action']

            # Attach action component to player entity.
            if action:
                self.world.add_component(2, ActionComponent(action=action)) # 2 is player entity
                self.world.remove_component(2, PlayerInputComponent)