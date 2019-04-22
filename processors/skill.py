import esper

from components.actor.equipment import EquipmentComponent
from components.actor.prepare_skill import PrepareSkillComponent
from components.item.skill import ItemSkillComponent
from components.item.slot import SlotComponent

class SkillProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (eqp, skill) in self.world.get_components(EquipmentComponent, PrepareSkillComponent):
            slot = skill.slot
            item_skill_component = None

            # Look to see if we have a valid item for that skill.
            for item in eqp.equipment:
                item_slot = self.world.components_for_entity(item, SlotComponent).slot
                item_skill_component = self.world.components_for_entity(item, ItemSkillComponent)

                if not item_skill_component:
                    continue
                elif ((slot == 'q' and item_slot == 'mainhand' and item_skill_component.skill) or
                    (slot == 'w' and item_slot == 'head' and item_skill_component.skill) or
                    (slot == 'e' and item_slot == 'accessory' and item_skill_component.skill) or
                    (slot == 'a' and item_slot == 'offhand' and item_skill_component.skill) or
                    (slot == 's' and item_slot == 'torso' and item_skill_component.skill) or
                    (slot == 'd' and item_slot == 'boots' and item_skill_component.skill)):
                    break

            else:
                # This has failed.
                self.world.events.append({'skill_done': True})
            
            # There is a skill that can be used here!

                