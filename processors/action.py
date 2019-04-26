import esper
import math

from components.actor.action import ActionComponent
from components.actor.consume import ConsumeComponent
from components.actor.descend import DescendComponent
from components.actor.drop import DropComponent
from components.actor.energy import EnergyComponent
from components.actor.open_inv import OpenInventoryComponent
from components.actor.pickup import PickupComponent
from components.actor.player import PlayerComponent
from components.actor.skill_execute import SkillExecutionComponent
from components.actor.skill_prepare import SkillPreparationComponent
from components.actor.remove import RemoveComponent
from components.actor.velocity import VelocityComponent
from components.actor.wait import WaitComponent
from components.actor.wear import WearComponent
from components.position import PositionComponent

class ActionProcessor(esper.Processor):
    ' The ActionProcessor adds and removes Components based on the action. '
    ' This, in turn, will cause various processors to change the update the game. '
    ' It is like the EventProcessor, but for the character and not the user. '
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (act) in self.world.get_component(ActionComponent):
            _consume = act.action.get('consume')
            _descend = act.action.get('descend')
            _drop = act.action.get('drop')
            _open_inventory = act.action.get('open_inventory')
            _mouse_move = act.action.get('mouse_move')
            _move = act.action.get('move')
            _pick_up = act.action.get('pick_up')
            _remove = act.action.get('remove')
            _skill_cancel = act.action.get('skill_cancel')
            _skill_execute = act.action.get('skill_execute')
            _skill_move = act.action.get('skill_move')
            _skill_prepare = act.action.get('skill_prepare')
            _wait = act.action.get('wait')
            _wear = act.action.get('wear')

            self.world.component_for_entity(ent, EnergyComponent).action = list(act.action.keys()).pop() # There should only be one action in the dict...

            if _consume:
                if _consume is True:
                    self.world.add_component(ent, ConsumeComponent(item_id=None))
                elif _consume:
                    self.world.add_component(ent, ConsumeComponent(item_id=_consume))
                    
            elif _descend:
                self.world.add_component(ent, DescendComponent())

            elif _drop:
                if _drop is True:
                    self.world.add_component(ent, DropComponent(item_id=None))
                elif _drop:
                    self.world.add_component(ent, DropComponent(item_id=_drop))    

            elif _open_inventory:
                self.world.add_component(ent, OpenInventoryComponent())

            elif _mouse_move:
                mx, my = _mouse_move.tile.x, _mouse_move.tile.y
                pos = self.world.component_for_entity(ent, PositionComponent)

                dx = mx - pos.x
                dy = my - pos.y
                r = math.sqrt( dx**2 + dy**2)

                self.world.add_component(ent, VelocityComponent(dx=round(dx/r), dy=round(dy/r)))
                self.world.create_dijkstra_map = True

            elif _move:
                dx, dy = _move
                self.world.add_component(ent, VelocityComponent(dx=dx, dy=dy))
                self.world.create_dijkstra_map = True
            
            elif _pick_up:
                if _pick_up is True:
                    self.world.add_component(ent, PickupComponent(item_id=None))
                elif _pick_up:
                    self.world.add_component(ent, PickupComponent(item_id=_pick_up))
                    
            elif _remove:
                self.world.add_component(ent, RemoveComponent(item_id=_remove))

            elif _skill_cancel:
                self.world.remove_component(ent, SkillPreparationComponent)
            
            elif _skill_execute:
                self.world.add_component(ent, SkillExecutionComponent())

            elif _skill_move:
                self.world.component_for_entity(ent, SkillPreparationComponent).direction = _skill_move

            elif _skill_prepare:
                if self.world.has_component(ent, SkillPreparationComponent):
                    prepped_skill = self.world.component_for_entity(ent, SkillPreparationComponent)
                    if _skill_prepare == prepped_skill.slot:
                        # Change the action... this does not occur often!
                        self.world.remove_component(ent, ActionComponent)
                        self.world.add_component(ent, ActionComponent({'skill_execute': True}))
                        return
                    else:
                        prepped_skill.slot = _skill_prepare
                else:
                    self.world.add_component(ent, SkillPreparationComponent(slot=_skill_prepare))

            elif _wait:
                self.world.add_component(ent, WaitComponent())

            elif _wear:
                if _wear is True:
                    self.world.add_component(ent, WearComponent(item_id=None))
                elif _wear:
                    self.world.add_component(ent, WearComponent(item_id=_wear))
                    
            self.world.remove_component(ent, ActionComponent)