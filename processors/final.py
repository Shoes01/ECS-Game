import esper

from components.game.processor import ProcessorComponent
from processors.initial import InitialProcessor

class FinalProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        if self.world._entities and self.world.component_for_entity(1, ProcessorComponent).final:
            self.world.clear_database()