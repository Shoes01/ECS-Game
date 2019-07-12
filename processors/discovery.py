import esper

from processors.render import RenderProcessor
from queue import Queue

class DiscoveryProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            if event.get('message'):
                message_contents = list((event.get('turn') + 1,))
                message_type, message_contents_partial = event['message']
                message_contents.extend(message_contents_partial)
                self.world.messages.append({message_type: message_contents})
                self.world.get_processor(RenderProcessor).queue.put({'redraw': True})