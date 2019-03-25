import esper

from components.game.debug import DebugComponent
from components.game.dijgen import DijgenComponent
from components.game.event import EventComponent
from components.game.map import MapComponent
from components.game.mapgen import MapgenComponent
from components.game.processor import ProcessorComponent
from components.game.state import StateComponent
from processors.initial import InitialProcessor
from processors.final import FinalProcessor

class EventProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):        
        event_component = self.world.component_for_entity(1, EventComponent)
        state_component = self.world.component_for_entity(1, StateComponent)
        
        if state_component.state == 'MainMenu':
            if event_component.event == 'Exit':
                state_component.state = 'Exit'
            if event_component.event == 'New_map':
                self.world.add_component(1, MapgenComponent())
                self.world.add_component(1, DijgenComponent())
                state_component.state = 'Game'

        if state_component.state == 'Game':
            if event_component.event == 'Exit':
                self.world.component_for_entity(1, ProcessorComponent).final = True
                state_component.state = 'MainMenu'
            if event_component.event == 'PlayerKilled':
                state_component.state = 'GameOver'
        
        if state_component.state == 'GameOver':
            if event_component.event == 'Exit':
                self.world.component_for_entity(1, ProcessorComponent).final = True
                state_component.state = 'MainMenu'

        # Special debug event
        if event_component.event == 'Toggle_debug_mode':
            if self.world.has_component(1, DebugComponent):
                self.world.remove_component(1, DebugComponent)
            else:
                self.world.add_component(1, DebugComponent())

        event_component.event = None