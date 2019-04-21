import esper
import tcod as libtcod
import tcod.event

from components.actor.action import ActionComponent
from components.actor.actor import ActorComponent
from components.actor.energy import EnergyComponent
from components.actor.player import PlayerComponent
from components.position import PositionComponent
from game import PopupMenu, PopupChoice

class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        action = None
        events = []
        state = self.world.state
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
            self.world.events.append({'mouse_pos': (mouse.tile.x, mouse.tile.y)})

        try:
            key_char = chr(key.sym)
        except:
            key_char = None

        if key:
            key_scancode = key.scancode

        ### INPUTS THAT ARE READ REGARDLESS OF TURN
        if key_char == 'd' and key.mod & libtcod.event.KMOD_CTRL:
            events.append({'toggle_debug': True})

        if state == 'PopupMenu':
            menu = self.world.popup_menus[-1]
            
            for choice in menu.contents:
                if key_char == choice.key:
                    if choice.action:
                        action = choice.result
                    else:
                        events.append(choice.result)
                    
                    if menu.auto_close:
                        events.append({'close_popup_menu': True})

            else:
                if menu.include_esc and key_scancode == libtcod.event.SCANCODE_ESCAPE:
                    events.append({'pop_popup_menu': True})
    
        elif state == 'MainMenu':
            if key_scancode == libtcod.event.SCANCODE_ESCAPE:
                events.append({'exit': True})
            elif key_scancode == libtcod.event.SCANCODE_KP_ENTER or key_scancode == libtcod.event.SCANCODE_RETURN:
                events.append({'new_map': True})
            elif key_char == 'l':
                events.append({'load_game': True})

        elif state == 'Game':
            if key_scancode == libtcod.event.SCANCODE_ESCAPE:
                menu = PopupMenu(title='What would you like to do?')
                menu.contents.append(PopupChoice(name='Load game', key='l', result={'load_game': True}, action=False))
                menu.contents.append(PopupChoice(name='Quit', key='q', result={'exit': True}, action=False))
                menu.contents.append(PopupChoice(name='Save game', key='s', result={'save_game': True}, action=False))
                events.append({'popup': menu})
            if key_char == 'm':
                events.append({'view_log': True})

        elif state == 'ViewLog':
            if key_scancode == libtcod.event.SCANCODE_UP or key_char == 'k' or key_scancode == libtcod.event.SCANCODE_KP_8:
                events.append({'scroll': +1})
            elif key_scancode == libtcod.event.SCANCODE_DOWN or key_char == 'j' or key_scancode == libtcod.event.SCANCODE_KP_2:
                events.append({'scroll': -1})
            elif key_scancode == libtcod.event.SCANCODE_ESCAPE:
                events.append({'exit': True})

        elif state == 'GameOver' or state == 'VictoryScreen':
            if key_scancode == libtcod.event.SCANCODE_ESCAPE:
                events.append({'exit': True})
        
        elif state == 'Look':
            events.append(generic_move_keys(key_char, key_scancode))
            if key_scancode == libtcod.event.SCANCODE_ESCAPE:
                events.append({'exit': True})

        
        ### INPUTS THAT ARE READ ONLY ON THE PLAYERS TURN
        for ent, (actor, eng, player) in self.world.get_components(ActorComponent, EnergyComponent, PlayerComponent):
            if state == 'Game' and eng.energy == 0:
                action = generic_move_keys(key_char, key_scancode)
                
                if key_char == 'd' and not key.mod:
                    action = {'drop': True}
                if key_char == 'e':
                    action = {'consume': True}
                if key_char == 'g':
                    action = {'pick_up': True}
                if key_char == 'i':
                    action = {'open_inventory': True}
                if key_char == 'w' or key_char == 'r':
                    action = {'wear': True}
                if key_char == '>' or key_char == '<':
                    action = {'descend': True}
                if key_char == 'x':
                    _pos = self.world.component_for_entity(ent, PositionComponent)
                    events.append({'look': (_pos.x, _pos.y)})
                
                if mouse_click:
                    action = {'mouse_move': mouse_click}

            # Attach action component to player entity. This ends their turn.
            if action:
                self.world.add_component(ent, ActionComponent(action=action))
        
        # Attach event component to world entity. It does not have to be the player's turn for this to happen.
        if events:
            self.world.events.extend(events)

def generic_move_keys(key_char, key_scancode):
    action = {}

    if   key_char == 'k' or key_scancode == libtcod.event.SCANCODE_KP_8 or key_scancode == libtcod.event.SCANCODE_UP:
        action = {'move': (0, -1)}
    elif key_char == 'j' or key_scancode == libtcod.event.SCANCODE_KP_2 or key_scancode == libtcod.event.SCANCODE_DOWN:
        action = {'move': (0, 1)}
    elif key_char == 'h' or key_scancode == libtcod.event.SCANCODE_KP_4 or key_scancode == libtcod.event.SCANCODE_LEFT:
        action = {'move': (-1, 0)}
    elif key_char == 'l' or key_scancode == libtcod.event.SCANCODE_KP_6 or key_scancode == libtcod.event.SCANCODE_RIGHT:
        action = {'move': (1, 0)}
    elif key_char == 'y' or key_scancode == libtcod.event.SCANCODE_KP_7:
        action = {'move': (-1, -1)}
    elif key_char == 'u' or key_scancode == libtcod.event.SCANCODE_KP_9:
        action = {'move': (1, -1)}
    elif key_char == 'b' or key_scancode == libtcod.event.SCANCODE_KP_1:
        action = {'move': (-1, 1)}
    elif key_char == 'n' or key_scancode == libtcod.event.SCANCODE_KP_3:
        action = {'move': (1, 1)}
    elif key_char == '.' or key_scancode == libtcod.event.SCANCODE_KP_5:
        action = {'wait': True}
    
    return action