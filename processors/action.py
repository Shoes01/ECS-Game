import esper
import math

from components.actor.action import ActionComponent
from components.actor.consume import ConsumeComponent
from components.actor.descend import DescendComponent
from components.actor.drop import DropComponent
from components.actor.open_inv import OpenInventoryComponent
from components.actor.pickup import PickupComponent
from components.actor.player import PlayerComponent
from components.actor.prepare_skill import PrepareSkillComponent
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
        for ent, (action) in self.world.get_component(ActionComponent):
            _consume = action.action.get('consume')
            _descend = action.action.get('descend')
            _drop = action.action.get('drop')
            _open_inventory = action.action.get('open_inventory')
            _mouse_move = action.action.get('mouse_move')
            _move = action.action.get('move')
            _pick_up = action.action.get('pick_up')
            _remove = action.action.get('remove')
            _skill_prepare = action.action.get('skill_prepare')
            _wait = action.action.get('wait')
            _wear = action.action.get('wear')

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
            
            elif _skill_prepare:
                if self.world.has_component(ent, PrepareSkillComponent):
                    prepped_skill = self.world.component_for_entity(ent, PrepareSkillComponent)
                    if _skill_prepare == prepped_skill.slot:
                        self.world.events.append({'skill_done': True})
                    else:
                        prepped_skill.slot = _skill_prepare
                self.world.add_component(ent, PrepareSkillComponent(slot=_skill_prepare))

            elif _wait:
                self.world.add_component(ent, WaitComponent())

            elif _wear:
                if _wear is True:
                    self.world.add_component(ent, WearComponent(item_id=None))
                elif _wear:
                    self.world.add_component(ent, WearComponent(item_id=_wear))
                    
            self.world.remove_component(ent, ActionComponent)