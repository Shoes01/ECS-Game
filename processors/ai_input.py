import esper

from components.actor.actor import ActorComponent
from components.actor.brain import BrainComponent
from components.actor.has_turn import HasTurnComponent
from components.player import PlayerComponent

class AiInputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (brain) in self.world.get_components(ActorComponent, BrainComponent):
            if not self.world.has_component(ent, PlayerComponent):
                self.take_turn()
        
        self.world.add_component(2, HasTurnComponent())
        self.world.remove_processor(AiInputProcessor)
    
    def take_turn(self):
        # print('AI thinks.')
        pass