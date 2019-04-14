import esper

from components.game.descend import DescendComponent
from components.game.mapgen import MapgenComponent

class DescendProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        if self.world.has_component(1, DescendComponent):
            self.world.add_component(1, MapgenComponent)