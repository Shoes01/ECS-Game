import esper
import numpy as np

# from processors.consumable import ConsumableProcessor
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
                # self.world.get_processor(ConsumableProcessor).queue.put({'consumed': self.jar})
                self.world.get_processor(StateProcessor).queue.put({'exit': True})
                self.soul = None
