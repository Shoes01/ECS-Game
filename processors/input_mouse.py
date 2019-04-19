import esper
import tcod as libtcod

from components.game.state import StateComponent

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