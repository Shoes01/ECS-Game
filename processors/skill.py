import esper
import numpy as np

from _data import ENTITY_COLORS
from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.equipment import EquipmentComponent
from components.actor.skill_execute import SkillExecutionComponent
from components.actor.skill_prepare import SkillPreparationComponent
from components.actor.velocity import VelocityComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent

class SkillProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (eqp, pos, skill) in self.world.get_components(EquipmentComponent, PositionComponent, SkillPreparationComponent):
            item_name = None
            item_skill_component = None
            skill_name = None
            slot = skill.slot

            has_item = False
            legal_target = False
            legal_item = False
            legal_tile = True
            
            # Look to see if we have a valid item for that skill.
            for item in eqp.equipment:
                if slot == self.world.component_for_entity(item, SlotComponent).slot:
                    has_item = True
                    item_name = self.world.component_for_entity(item, NameComponent)._name
                    if self.world.has_component(item, ItemSkillComponent):
                        item_skill_component = self.world.component_for_entity(item, ItemSkillComponent)
                        legal_item = True
                        skill_name = item_skill_component.name
                        break
            else:
                # We have failed to find an item, or to find an item with a skill.
                self.world.messages.append({'skill': (has_item, legal_item, legal_target, legal_tile, item_name, self.world.turn)})
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
            
            entities_to_attack = []
            tile_destination = []

            for y in range(0, array_of_effect.shape[1]):
                for x in range(0, array_of_effect.shape[0]):
                    adjusted_x = xc + x - len(array_of_effect) // 2
                    adjusted_y = yc + y - len(array_of_effect) // 2
                    
                    entities = self.world.get_entities_at(adjusted_x, adjusted_y)

                    #tile = self.world.get_entities_at(adjusted_x, adjusted_y, TileComponent).pop()
                    #tile_ren = self.world.component_for_entity(tile, RenderComponent)

                    number = array_of_effect[y][x]
                    skill = 'skill_' + str(number)
                    
                    for entity in entities:
                        # Classify the entity first.
                        actor = False
                        floor = False
                        wall = False
                        
                        if self.world.has_component(entity, ActorComponent):
                            actor = True

                        elif self.world.has_component(entity, TileComponent):
                            tile_component = self.world.component_for_entity(entity, TileComponent)
                            self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS.get(skill) # Color the tile; this will be undone of the number == 0

                            if tile_component.blocks_path:
                                wall = tile_component
                            else:
                                floor = tile_component

                        ### Figure out if the skill happens!
                        if number == 0: # This tile is not part of the skill.
                            if wall:
                                wall.highlight_color = None
                            elif floor:
                                floor.highlight_color = None
                        
                        elif number == 1: # This skill deals damage to entities.
                            if actor:
                                entities_to_attack.append(entity)
                                legal_target = True

                        elif number == 2: # This skill deals damage to entities. This skill is blocked by terrain.
                            if actor:
                                entities_to_attack.append(entity)
                            elif wall:
                                legal_tile = False
                                self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']
                            
                        elif number == 3: # This skill moves the acting entity to this location. This skill is blocked by terrain.
                            if floor:
                                tile_destination.append(entity)
                                legal_target = True
                            elif actor or wall:
                                legal_tile = False
                                self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']
                            
                        elif number == 4: # This skill does nothing on its own. This skill is blocked by terrain and actors.
                            if wall or actor:
                                legal_tile = False
                                self.world.component_for_entity(entity, RenderComponent).highlight_color = ENTITY_COLORS['skill_blocked']
            
            if self.world.has_component(ent, SkillExecutionComponent):
                self.world.component_for_entity(ent, SkillExecutionComponent).cost = item_skill_component.cost
                
                if entities_to_attack and legal_tile:
                    # Do this skill!    
                    self.world.add_component(ent, CombatComponent(defender_IDs=entities_to_attack))
                elif tile_destination and legal_tile:
                    # Do this skill!
                    tile = tile_destination.pop()
                    tile_pos = self.world.component_for_entity(tile, PositionComponent)
                    ent_pos = self.world.component_for_entity(ent, PositionComponent)
                    dx = tile_pos.x - ent_pos.x
                    dy = tile_pos.y - ent_pos.y
                    self.world.add_component(ent, VelocityComponent(dx=dx, dy=dy)) 
                    self.world.remove_component(ent, SkillExecutionComponent)
                else:
                    self.world.remove_component(ent, SkillExecutionComponent)
                
                self.world.messages.append({'skill': (has_item, legal_item, legal_target, legal_tile, skill_name, self.world.turn)})
                self.world.remove_component(ent, SkillPreparationComponent)
                self.world.events.append({'skill_done': True})