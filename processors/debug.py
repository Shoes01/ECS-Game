import esper
import numpy as np
import tcod as libtcod

from processors.ai_input import AiInputProcessor
from processors.render import RenderProcessor

class DebugProcessor(esper.Processor):
    def __init_(self):
        super().__init__()
    
    def process(self):
        if self.world.get_processor(AiInputProcessor):
            dijkstra_map = self.world.get_processor(AiInputProcessor).dijkstra_map
            console = self.world.get_processor(RenderProcessor).console

            for (x, y), value in np.ndenumerate(dijkstra_map):
                if value == 999:
                    console.print(x, y, '#', libtcod.pink)
                else:
                    console.print(x, y, baseN(value, 35), libtcod.pink)
            
            console.blit(console)
            libtcod.console_flush()

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])