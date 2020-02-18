import esper

from components.actor.equipment import EquipmentComponent
from components.actor.skill_directory import SkillDirectoryComponent
from components.item.jobreq import JobReqComponent
from components.name import NameComponent
from components.item.skill_pool import SkillPoolComponent
from processors.energy import EnergyProcessor
from processors.skill_menu import SkillMenuProcessor
from processors.skill import SkillProcessor

from queue import Queue

class RemovableProcessor(esper.Processor):
    ' This processor is a sister-processor to Wearable. WearableProcessor contains the popup menu logic. '
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            free = event.get('free')
            item = event.get('item')
            job = event.get('new_job')

            eqp = self.world.component_for_entity(ent, EquipmentComponent)
            name_component = None if item is None else self.world.component_for_entity(item, NameComponent)
            turn = self.world.turn

            if item:
                # Remove the item, if it is equipped.
                success = False
                if item in eqp.equipment:
                    success = True
                    eqp.equipment.remove(item)                
                    name_component.name = name_component.original_name
                    if free is not True:
                        self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'remove': True})                
                self.world.messages.append({'remove': (name_component.name, success, turn)})

                # Deactivate all skills from this item, if they are not mastered.
                item_skills = self.world.component_for_entity(item, SkillPoolComponent).skill_pool
                for entity_skill in self.world.component_for_entity(ent, SkillDirectoryComponent).skill_directory:
                    if not entity_skill.is_mastered and entity_skill in item_skills:
                        self.world.get_processor(SkillMenuProcessor).queue.put({'ent': ent, 'skill_deactivate': entity_skill})

            elif job:
                # The player switched jobs; go through the equipped items to see if the player is still the correct job.
                for item in eqp.equipment:
                    if job not in self.world.component_for_entity(item, JobReqComponent).job_req:
                        self.queue.put({'ent': ent, 'item': item, 'free': True})