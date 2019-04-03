import esper

from components.actor.action import ActionComponent
from components.actor.equip import EquipComponent
from components.actor.player import PlayerComponent
from components.actor.velocity import VelocityComponent
from components.game.dijgen import DijgenComponent
from components.game.turn_count import TurnCountComponent

class ActionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (action) in self.world.get_component(ActionComponent):
            _move = action.action.get('move')
            _pick_up = action.action.get('pick_up')
            _wait = action.action.get('wait')

            if _move:
                dx, dy = _move
                self.world.add_component(ent, VelocityComponent(dx=dx, dy=dy))
                self.world.add_component(1, DijgenComponent())
            
            if _pick_up:
                self.world.add_component(ent, EquipComponent())

            if _wait:
                pass

            if ent == 2:
                self.world.component_for_entity(1, TurnCountComponent).turn_count += 1

            self.world.remove_component(ent, ActionComponent)