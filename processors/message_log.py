import esper

from components.game.message_log import MessageLogComponent

class MessageLogProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self._consoles = {}

    def process(self):
        message_log = self.world.component_for_entity(1, MessageLogComponent).messages
        console, x, y, w, h = self._consoles['log'] # type: (console, x, y, w, h)
        
        message_log = message_log[::-1]

        dy = 0
        for message in message_log:
            string, color = message
            console.print(0, 0 + dy, string, color)
            dy += 1
        
        console.blit(dest=self._consoles['con'][0], dest_x=x, dest_y=y, src_x=0, src_y=0, width=w, height=h)