import esper

from components.game.end_game import EndGameComponent
from processors.initial import InitialProcessor

class FinalProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        if self.world._entities and self.world.has_component(1, EndGameComponent):
            self.world.clear_database()