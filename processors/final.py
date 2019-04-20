import esper

from processors.initial import InitialProcessor

class FinalProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        if self.world._entities and self.world.clear_database:
            self.world.clear_database = False
            self.world.clear_database()