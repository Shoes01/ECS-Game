import esper

from components.actor.equipment import EquipmentComponent
from components.actor.prepare_skill import PrepareSkillComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent
from components.position import PositionComponent
from components.render import RenderComponent
from components.tile import TileComponent

class SkillProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (eqp, pos, skill) in self.world.get_components(EquipmentComponent, PositionComponent, PrepareSkillComponent):
            slot = skill.slot
            item_skill_component = None

            # Look to see if we have a valid item for that skill.
            for item in eqp.equipment:
                item_slot = self.world.components_for_entity(item, SlotComponent).slot
                item_skill_component = self.world.components_for_entity(item, ItemSkillComponent)

                if not item_skill_component:
                    continue
                elif ((slot == 'q' and item_slot == 'mainhand') or
                    (slot == 'w' and item_slot == 'head') or
                    (slot == 'e' and item_slot == 'accessory') or
                    (slot == 'a' and item_slot == 'offhand') or
                    (slot == 's' and item_slot == 'torso') or
                    (slot == 'd' and item_slot == 'boots') or
                    break

            else:
                # This has failed.
                self.world.events.append({'skill_done': True})
            
            # There is a skill that can be used here!
            # Fetch direction
            x, y = skill.direction
            hor = None
            ver = None
            direction = None

            if x == -1:
                hor = 'east'
            elif x == 1:
                hor == 'west'
            
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

            # Set the tiles to have their bg colors changes.
            xc, yc = pos.x, pos.y
            
            for x in range(len(array_of_effect)):
                for y in range(len(array_of_effect)):
                    if array_of_effect[y][x]:
                        adjusted_x = xc + x - len(array_of_effect) // 2
                        adjusted_y = yc + y - len(array_of_effect) // 2

                        tile = self.world.get_entities_at(adjusted_x, adjusted_y, TileComponent).pop()
                        self.world.component_for_entity(tile, RenderComponent).targeted = True


            


                