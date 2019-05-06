import esper

from components.stairs import StairsComponent
from components.position import PositionComponent
from processors.energy import EnergyProcessor
from queue import Queue

class DescendProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']

            pos = self.world.component_for_entity(ent, PositionComponent)

            # Look to see if we are standing on stairs.
            for stairs, (s_pos, _) in self.world.get_components(PositionComponent, StairsComponent):
                if pos.x == s_pos.x and pos.y == s_pos.y:
                    self.world.events.append({'new_map': True})
                    self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'descend': True})
                    break