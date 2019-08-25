import esper

from components.actor.equipment import EquipmentComponent
from components.actor.skill_directory import SkillDirectoryComponent
from components.item.skill import ItemSkillComponent
from queue import Queue

class SkillDirectoryProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ap_gain = event.get('ap_gain')
            item = event.get('item')
            new_skill = event.get('new_skill')
            ent = event['ent']
            skill = event.get('skill')

            sd_comp = self.world.component_for_entity(ent, SkillDirectoryComponent)

            if new_skill:
                skill = None if not self.world.has_component(item, ItemSkillComponent) else self.world.component_for_entity(item, ItemSkillComponent) 
                
                if skill and skill.name not in sd_comp.skill_directory.keys():
                    sd_comp.skill_directory[skill.name] = (0, skill.ap_max)

            elif ap_gain:
                # Go through each item that is equipped, and add AP to its skill.
                eqp_comp = self.world.component_for_entity(ent, EquipmentComponent)
                for item in eqp_comp.equipment:
                    skill = None if not self.world.has_component(item, ItemSkillComponent) else self.world.component_for_entity(item, ItemSkillComponent) 
                    
                    if skill is not None:
                        ap_current, ap_max = sd_comp.skill_directory[skill.name]
                        ap_current += ap_gain

                        if ap_current > ap_max:
                            ap_current = ap_max

                        sd_comp.skill_directory[skill.name] = (ap_current, ap_max)