import esper

from components.actor.actor import ActorComponent
from components.actor.has_turn import HasTurnComponent
from components.actor.waiting_turn import WaitingTurnComponent

class TurnProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (actor, wait) in self.world.get_components(ActorComponent, WaitingTurnComponent):
            if wait.ticks > 0:
                wait.ticks -= 1
            elif wait.ticks == 0:
                self.world.add_component(ent, HasTurnComponent())