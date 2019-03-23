import esper

from components.game.event import EventComponent
from components.game.mapgen import MapgenComponent
from components.game.state import StateComponent
from processors.debug import DebugProcessor
from processors.dijkstra import DijkstraProcessor
from processors.render import RenderProcessor

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):        
        event_component = self.world.component_for_entity(1, EventComponent)
        state_component = self.world.component_for_entity(1, StateComponent)
        # print('Event: {0}. State: {1}.'.format(event_component.event, state_component.state)) # Debug code
        
        if state_component.state == 'MainMenu':
            if event_component.event == 'Exit':
                state_component.state = 'Exit'
            if event_component.event == 'New_map':
                self.world.add_component(1, MapgenComponent())
                state_component.state = 'Game'

        if state_component.state == 'Game':
            if event_component.event == 'Exit':
                state_component.state = 'MainMenu'
                self.world.remove_processor(DijkstraProcessor)
        
        # Special debug event
        if event_component.event == 'Toggle_debug_mode':
            debug_processor = self.world.get_processor(DebugProcessor)

            if debug_processor:
                debug_processor.kill()
                self.world.remove_processor(DebugProcessor)
            else:
                self.world.add_processor(DebugProcessor(), 39)

        event_component.event = None