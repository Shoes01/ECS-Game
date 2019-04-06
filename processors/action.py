import esper

from components.actor.action import ActionComponent
from components.actor.equip import EquipComponent
from components.actor.player import PlayerComponent
from components.actor.velocity import VelocityComponent
from components.actor.wait import WaitComponent
from components.game.dijgen import DijgenComponent
from components.game.turn_count import TurnCountComponent

class ActionProcessor(esper.Processor):
    ' The ActionProcessor adds and removes Components based on the action. '
    ' This, in turn, will cause various processors to change the update the game. '
    ' It is like the EventProcessor, but for the character and not the user. '
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
                if _pick_up is not True:
                    self.world.add_component(ent, EquipComponent(item_id=_pick_up))
                else:
                    self.world.add_component(ent, EquipComponent(item_id=None))

            if _wait:
                self.world.add_component(ent, WaitComponent())

            if ent == 2:
                self.world.component_for_entity(1, TurnCountComponent).turn_count += 1

            self.world.remove_component(ent, ActionComponent)