import esper
import tcod as libtcod

from components.actor.action import ActionComponent
from components.actor.actor import ActorComponent
from components.actor.energy import EnergyComponent
from components.actor.player import PlayerComponent
from components.game.event import EventComponent
from components.game.popup import PopupComponent
from components.game.state import StateComponent

class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._key = None
        self._mouse = None
    
    def process(self):
        action = None
        event = None
        game_state_component = self.world.component_for_entity(1, StateComponent)
        key = self._key
        key_char = chr(key.c)
        mouse = self._mouse

        if key.vk is libtcod.KEY_NONE:
            return 0

        if key_char == 'd' and key.lctrl:
            event = {'toggle_debug': True}

        ### INPUTS THAT ARE READ REGARDLESS OF TURN
        if game_state_component.state == 'PopupMenu':
            _popup_comp = self.world.component_for_entity(1, PopupComponent)
            for choice in _popup_comp.choices:
                _, valid_key, result = choice
                if key_char == valid_key:
                    if result.get('event'):
                        event = result['event']
                        event = {'close_popup_menu': True}
                        break
                    if result.get('action'):
                        action = result['action']
                        event = {'close_popup_menu': True}
                        break
                elif key.vk == libtcod.KEY_ESCAPE:
                    event = {'close_popup_menu': True}
                    break
    
        if game_state_component.state == 'MainMenu':
            if key.vk == libtcod.KEY_ESCAPE:
                event = {'exit': True}
            elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:
                event = {'new_map': True}

        elif game_state_component.state == 'Game':
            if key.vk == libtcod.KEY_ESCAPE:
                popup_component = PopupComponent(
                    title='Are you sure you want to quit?',
                    choices=[
                        (
                            'Yes',
                            'y',
                            {'event': {'exit': True}}
                        ),
                        (
                            'No',
                            'n',
                            {'event': {'close_popup_menu': True}}
                        )
                    ]
                )
                event = {'popup_menu': popup_component}

        elif game_state_component.state == 'GameOver':
            if key.vk == libtcod.KEY_ESCAPE:
                    event = {'exit': True}

        ### INPUTS THAT ARE READ ONLY ON THE PLAYERS TURN
        for ent, (actor, eng, player) in self.world.get_components(ActorComponent, EnergyComponent, PlayerComponent):
            if game_state_component.state == 'Game':
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

            # Attach action component to player entity. This ends their turn.
            if action:
                self.world.add_component(ent, ActionComponent(action=action))
        
        # Attach event component to world entity. It does not have to be the player's turn for this to happen.
        if event:
            self.world.add_component(1, EventComponent(event=event)) # 1 is world entity
