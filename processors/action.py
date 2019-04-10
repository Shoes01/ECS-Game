import esper

from components.actor.action import ActionComponent
from components.actor.consume import ConsumeComponent
from components.actor.drop import DropComponent
from components.actor.open_inv import OpenInventoryComponent
from components.actor.pickup import PickupComponent
from components.actor.player import PlayerComponent
from components.actor.velocity import VelocityComponent
from components.actor.wait import WaitComponent
from components.actor.wear import WearComponent
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
            _consume = action.action.get('consume')
            _drop = action.action.get('drop')
            _open_inventory = action.action.get('open_inventory')
            _move = action.action.get('move')
            _pick_up = action.action.get('pick_up')
            _wait = action.action.get('wait')
            _wear = action.action.get('wear')

            if _consume:
                if _consume is not True:
                    self.world.add_component(ent, ConsumeComponent(item_id=_consume))
                else:
                    self.world.add_component(ent, ConsumeComponent(item_id=None))

            if _drop:
                if _drop is not True:
                    self.world.add_component(ent, DropComponent(item_id=_drop))    
                else:
                    self.world.add_component(ent, DropComponent(item_id=None))
                
            if _open_inventory:
                self.world.add_component(ent, OpenInventoryComponent())

            if _move:
                dx, dy = _move
                self.world.add_component(ent, VelocityComponent(dx=dx, dy=dy))
                self.world.add_component(1, DijgenComponent())
            
            if _pick_up:
                if _pick_up is not True:
                    self.world.add_component(ent, PickupComponent(item_id=_pick_up))
                else:
                    self.world.add_component(ent, PickupComponent(item_id=None))

            if _wait:
                self.world.add_component(ent, WaitComponent())

            if _wear:
                if _wear is not True:
                    self.world.add_component(ent, WearComponent(item_id=_wear))
                else:
                    self.world.add_component(ent, WearComponent(item_id=None))

            self.world.remove_component(ent, ActionComponent)