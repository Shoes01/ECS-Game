import esper
import tcod as libtcod
import tcod.event

from components.actor.action import ActionComponent
from components.actor.actor import ActorComponent
from components.actor.energy import EnergyComponent
from components.actor.player import PlayerComponent
from components.game.events import EventsComponent
from components.game.popup import PopupComponent, PopupMenu, PopupChoice
from components.game.state import StateComponent
from processors.debug import DebugProcessor

class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        action = None
        events = []
        game_state_component = self.world.component_for_entity(1, StateComponent)
        key = None
        key_char = None
        mouse = None

        for event in libtcod.event.get():
            if event.type == 'KEYDOWN':
                key = event
            elif event.type == 'MOUSEMOTION':
                mouse = event

        self.world.get_processor(DebugProcessor)._input = (key, mouse)

        if key is None:
            return 0

        try:
            key_char = chr(key.sym)
        except:
            key_char = None

        ### INPUTS THAT ARE READ REGARDLESS OF TURN
        if key_char == 'd' and key.mod & libtcod.event.KMOD_CTRL:
            events.append({'toggle_debug': True})

        if game_state_component.state == 'PopupMenu':
            menu = self.world.component_for_entity(1, PopupComponent).menus[-1]
            
            for choice in menu.contents:
                if key_char == choice.key:
                    if choice.action:
                        action = choice.result
                    else:
                        events.append(choice.result)
                    
                    if menu.auto_close:
                        events.append({'close_popup_menu': True})

            else:
                if menu.include_esc and key.scancode == libtcod.event.SCANCODE_ESCAPE:
                    events.append({'pop_popup_menu': True})
    
        elif game_state_component.state == 'MainMenu':
            if key.scancode == libtcod.event.SCANCODE_ESCAPE:
                events.append({'exit': True})
            elif key.scancode == libtcod.event.SCANCODE_KP_ENTER or key.scancode == libtcod.event.SCANCODE_RETURN:
                events.append({'new_map': True})
            elif key_char == 'l':
                events.append({'load_game': True})

        elif game_state_component.state == 'Game':
            if key.scancode == libtcod.event.SCANCODE_ESCAPE:
                menu = PopupMenu(title='What would you like to do?')
                menu.contents.append(PopupChoice(name='Load game', key='l', result={'load_game': True}, action=False))
                menu.contents.append(PopupChoice(name='Quit', key='q', result={'exit': True}, action=False))
                menu.contents.append(PopupChoice(name='Save game', key='s', result={'save_game': True}, action=False))
                events.append({'popup': menu})

        elif game_state_component.state == 'GameOver':
            if key.scancode == libtcod.event.SCANCODE_ESCAPE:
                    events.append({'exit': True})

        ### INPUTS THAT ARE READ ONLY ON THE PLAYERS TURN
        for ent, (actor, eng, player) in self.world.get_components(ActorComponent, EnergyComponent, PlayerComponent):
            if game_state_component.state == 'Game' and eng.energy == 0:
                if key.scancode == libtcod.event.SCANCODE_UP or key_char == 'k' or key.scancode == libtcod.event.SCANCODE_KP_8:
                    action = {'move': (0, -1)}
                elif key.scancode == libtcod.event.SCANCODE_DOWN or key_char == 'j' or key.scancode == libtcod.event.SCANCODE_KP_2:
                    action = {'move': (0, 1)}
                elif key.scancode == libtcod.event.SCANCODE_LEFT or key_char == 'h' or key.scancode == libtcod.event.SCANCODE_KP_4:
                    action = {'move': (-1, 0)}
                elif key.scancode == libtcod.event.SCANCODE_RIGHT or key_char == 'l' or key.scancode == libtcod.event.SCANCODE_KP_6:
                    action = {'move': (1, 0)}
                elif key_char == 'y' or key.scancode == libtcod.event.SCANCODE_KP_7:
                    action = {'move': (-1, -1)}
                elif key_char == 'u' or key.scancode == libtcod.event.SCANCODE_KP_9:
                    action = {'move': (1, -1)}
                elif key_char == 'b' or key.scancode == libtcod.event.SCANCODE_KP_1:
                    action = {'move': (-1, 1)}
                elif key_char == 'n' or key.scancode == libtcod.event.SCANCODE_KP_3:
                    action = {'move': (1, 1)}
                elif key_char == '.' or key.scancode == libtcod.event.SCANCODE_KP_5:
                    action = {'wait': True}
                
                if key_char == 'd':
                    action = {'drop': True}
                if key_char == 'e':
                    action = {'consume': True}
                if key_char == 'g':
                    action = {'pick_up': True}
                if key_char == 'i':
                    action = {'open_inventory': True}
                if key_char == 'w' or key_char == 'r':
                    action = {'wear': True}

            # Attach action component to player entity. This ends their turn.
            if action:
                self.world.add_component(ent, ActionComponent(action=action))
        
        # Attach event component to world entity. It does not have to be the player's turn for this to happen.
        if events:
            self.world.add_component(1, EventsComponent(events=events)) # 1 is world entity
