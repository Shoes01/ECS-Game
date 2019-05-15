import esper

from queue import Queue

class FinalProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            if event.get('reset_game'):
                self.world.clear_database()