import esper
import tcod as libtcod
import tcod.event

from components.actor.actor import ActorComponent
from components.actor.energy import EnergyComponent
from components.actor.player import PlayerComponent
from components.position import PositionComponent
from menu import PopupMenu, PopupChoice
from processors.action import ActionProcessor
from processors.debug import DebugProcessor
from processors.mapgen import MapgenProcessor
from processors.state import StateProcessor
from processors.render import RenderProcessor

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

        if key or mouse_click:
            self.world.get_processor(DebugProcessor).queue.put({'redraw': True})
            self.world.get_processor(RenderProcessor).queue.put({'redraw': True})

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
                        self.world.get_processor(StateProcessor).queue.put(choice.result)
                        # events.append(choice.result) # what is this
                    
                    if menu.auto_close:
                        self.world.get_processor(StateProcessor).queue.put({'exit': True})

            else:
                if menu.include_esc and key_scancode == libtcod.event.SCANCODE_ESCAPE:
                    self.world.get_processor(StateProcessor).queue.put({'pop': True})
    
        elif state == 'MainMenu':
            if key_scancode == libtcod.event.SCANCODE_ESCAPE:
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
            elif key_scancode == libtcod.event.SCANCODE_KP_ENTER or key_scancode == libtcod.event.SCANCODE_RETURN:
                self.world.get_processor(MapgenProcessor).queue.put({'generate_map': True})
                self.world.get_processor(StateProcessor).queue.put({'generate_map': True})
            elif key_char == 'l':
                events.append({'load_game': True})

        elif state == 'Game':
            if key_scancode == libtcod.event.SCANCODE_ESCAPE:
                menu = PopupMenu(title='What would you like to do?')
                menu.contents.append(PopupChoice(name='Load game', key='l', result={'load_game': True}, action=False))
                menu.contents.append(PopupChoice(name='Quit', key='q', result={'exit': True}, action=False))
                menu.contents.append(PopupChoice(name='Save game', key='s', result={'save_game': True}, action=False))
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})
            if key_char == 'm':
                self.world.get_processor(StateProcessor).queue.put({'view_log': True})

        elif state == 'ViewLog':
            if key_scancode == libtcod.event.SCANCODE_UP or key_char == 'k' or key_scancode == libtcod.event.SCANCODE_KP_8:
                events.append({'scroll': +1})
            elif key_scancode == libtcod.event.SCANCODE_DOWN or key_char == 'j' or key_scancode == libtcod.event.SCANCODE_KP_2:
                events.append({'scroll': -1})
            elif key_scancode == libtcod.event.SCANCODE_ESCAPE:
                self.world.get_processor(StateProcessor).queue.put({'exit': True})

        elif state == 'GameOver' or state == 'VictoryScreen':
            if key_scancode == libtcod.event.SCANCODE_ESCAPE:
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
        
        elif state == 'Look':
            events.append(generic_move_keys(key_char, key_scancode))
            if key_scancode == libtcod.event.SCANCODE_ESCAPE:
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
        
        elif state == 'SkillTargeting':
            action = generic_move_keys(key_char, key_scancode)
            if action:
                action['skill_move'] = action['move']
                action['move'] = None
            elif key_scancode == libtcod.event.SCANCODE_ESCAPE:
                action = {'skill_cancel': True}
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
            elif key_char == 'q':
                action = {'skill_prepare': 'mainhand'}
            elif key_char == 'w':
                action = {'skill_prepare': 'head'}
            elif key_char == 'e':
                action = {'skill_prepare': 'accessory'}
            elif key_char == 'a':
                action = {'skill_prepare': 'offhand'}
            elif key_char == 's':
                action = {'skill_prepare': 'torso'}
            elif key_char == 'd':
                action = {'skill_prepare': 'feet'}
            elif key_scancode == libtcod.event.SCANCODE_SPACE:
                action = {'skill_execute': True}

        ### INPUTS THAT ARE READ ONLY ON THE PLAYERS TURN
        for ent, (actor, eng, player) in self.world.get_components(ActorComponent, EnergyComponent, PlayerComponent):
            if state == 'Game' and eng.energy == 0:
                # Movement keys.
                action = generic_move_keys(key_char, key_scancode)
                
                # Other keys.
                if key_char == 'd' and key.mod & libtcod.event.KMOD_SHIFT:
                    action = {'drop': True}
                elif key_char == 'e' and key.mod & libtcod.event.KMOD_SHIFT:
                    action = {'consume': True}
                elif key_char == 'g':
                    action = {'pick_up': True}
                elif key_char == 'i':
                    action = {'open_inventory': True}
                elif (key_char == 'w' and key.mod & libtcod.event.KMOD_SHIFT) or key_char == 'r':
                    action = {'wear': True}
                elif key_char == '>' or key_char == '<':
                    action = {'descend': True}
                elif key_char == 'x':
                    _pos = self.world.component_for_entity(ent, PositionComponent)
                    events.append({'look': (_pos.x, _pos.y)})

                # Skill keys.
                elif key_char == 'q':
                    action = {'skill_prepare': 'mainhand'}
                elif key_char == 'w':
                    action = {'skill_prepare': 'head'}
                elif key_char == 'e':
                    action = {'skill_prepare': 'accessory'}
                elif key_char == 'a':
                    action = {'skill_prepare': 'offhand'}
                elif key_char == 's':
                    action = {'skill_prepare': 'torso'}
                elif key_char == 'd':
                    action = {'skill_prepare': 'feet'}
                
                # Mouse movement.
                if mouse_click:
                    action = {'mouse_move': mouse_click}

            # Attach action component to player entity. This ends their turn.
            if action:
                action['ent'] = 1
                self.world.get_processor(ActionProcessor).queue.put(action)
        
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