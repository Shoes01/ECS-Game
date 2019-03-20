import esper

from components.action import Action
from components.player import Player
from components.turn import Turn

class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.action = None
    
    def process(self):
        if self.action:
            for ent, (player, turn) in self.world.get_components(Player, Turn):
                self.world.add_component(ent, Action(self.action))