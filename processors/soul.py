import esper
import numpy as np
import processors.consumable # This is to avoid a cyclical import.

from components.soul import SoulComponent
from processors.state import StateProcessor
from queue import Queue

class SoulProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self.jar = None
        self.soul = None
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            cancel = event.get('cancel')
            ent = event.get('ent')
            confirm = event.get('confirm')
            jar = event.get('jar')
            rotate = event.get('rotate')
            soul = event.get('soul')

            if soul:
                self.world.get_processor(StateProcessor).queue.put({'soul_state': True})
                self.jar = jar
                self.soul = soul

            if rotate:
                dx, dy = rotate
                if dx:
                    self.soul.np_soul = np.fliplr(self.soul.np_soul)
                if dy:
                    self.soul.np_soul = np.flipud(self.soul.np_soul)

            if confirm:
                # Add the soul to the player's soul
                self.world.component_for_entity(ent, SoulComponent).np_soul += self.soul.np_soul
                self.world.get_processor(processors.consumable.ConsumableProcessor).queue.put({'ent': ent, 'consumed': self.jar})
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
                self.jar = None
                self.soul = None

            if cancel:
                self.jar = None
                self.soul = None