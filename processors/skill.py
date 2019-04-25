import esper
import numpy as np

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.equipment import EquipmentComponent
from components.actor.skill_execute import SkillExecutionComponent
from components.actor.skill_prepare import SkillPreparationComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent

class SkillProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (eqp, pos, skill) in self.world.get_components(EquipmentComponent, PositionComponent, SkillPreparationComponent):
            slot = skill.slot
            item_skill_component = None
            skill_name = None

            # Look to see if we have a valid item for that skill.
            for item in eqp.equipment:
                item_slot = self.world.component_for_entity(item, SlotComponent).slot
                
                if self.world.has_component(item, ItemSkillComponent):
                    item_skill_component = self.world.component_for_entity(item, ItemSkillComponent)
                else:
                    continue

                if ((slot == 'q' and item_slot == 'mainhand') or
                    (slot == 'w' and item_slot == 'head') or
                    (slot == 'e' and item_slot == 'accessory') or
                    (slot == 'a' and item_slot == 'offhand') or
                    (slot == 's' and item_slot == 'torso') or
                    (slot == 'd' and item_slot == 'feet')):
                    skill_name = item_skill_component.name
                    break

            else:
                # This has failed.
                legal_target = True
                legal_item = False
                legal_tile = True
                self.world.messages.append({'skill': (legal_item, legal_target, legal_tile, skill_name, self.world.turn)})
                self.world.remove_component(ent, SkillPreparationComponent)
                self.world.events.append({'skill_done': True})
                return 0
            
            # Fetch direction
            x, y = skill.direction
            hor = None
            ver = None
            direction = None

            if x == 1:
                hor = 'east'
            elif x == -1:
                hor = 'west'
            
            if y == -1:
                ver = 'north'
            elif y == 1:
                ver = 'south'
            
            if hor and ver:
                direction = ver + '_' + hor
            elif hor:
                direction = hor
            elif ver:
                direction = ver
            
            array_of_effect = item_skill_component.__dict__[direction]

            # Set the tiles to have their bg colors changes, and fetch the entities on those tiles.
            xc, yc = pos.x, pos.y
            
            entities_targeted = []
            legal_tile = True
            for y in range(0, array_of_effect.shape[1]):
                for x in range(0, array_of_effect.shape[0]):
                    adjusted_x = xc + x - len(array_of_effect) // 2
                    adjusted_y = yc + y - len(array_of_effect) // 2
                    
                    tile = self.world.get_entities_at(adjusted_x, adjusted_y, TileComponent).pop()
                    tile_ren = self.world.component_for_entity(tile, RenderComponent)

                    if array_of_effect[y][x] == 0:
                        tile_ren.highlight_color = None
                    else:
                        number = array_of_effect[y][x]
                        string = 'skill_' + str(number)
                        
                        ### Choose how to highlight the tiles.
                        entities = self.world.get_entities_at(adjusted_x, adjusted_y)
                        # Assume it works.
                        tile_ren.highlight_color = ENTITY_COLORS[string] 
                        # Now look for problems.
                        for entity in entities:
                            actor = self.world.has_component(entity, ActorComponent)
                            if actor:
                                entities_targeted.append(entity)
                            wall = False
                            if self.world.has_component(entity, TileComponent) and self.world.component_for_entity(entity, TileComponent).blocks_path:
                                wall = True
                            
                            if number == 2 and wall:
                                legal_tile = False
                                tile_ren.highlight_color = ENTITY_COLORS['skill_blocked']
                            elif number == 4 and (wall or actor):
                                legal_tile = False
                                tile_ren.highlight_color = ENTITY_COLORS['skill_blocked']
            
            if self.world.has_component(ent, SkillExecutionComponent):
                self.world.component_for_entity(ent, SkillExecutionComponent).cost = item_skill_component.cost
                if entities_targeted and legal_tile:
                    # Do this skill!
                    legal_target = True
                    legal_item = True
                    self.world.messages.append({'skill': (legal_item, legal_target, legal_tile, skill_name, self.world.turn)})
                    self.world.add_component(ent, CombatComponent(defender_IDs=entities_targeted))
                else:
                    legal_target = False
                    legal_item = True
                    self.world.messages.append({'skill': (legal_item, legal_target, legal_tile, skill_name, self.world.turn)})
                    self.world.remove_component(ent, SkillExecutionComponent)
                self.world.remove_component(ent, SkillPreparationComponent)
                self.world.events.append({'skill_done': True})