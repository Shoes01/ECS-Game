import esper

from components.actor.job import JobComponent
from components.actor.skill_directory import SkillDirectoryComponent
from components.item.skill_pool import SkillPoolComponent
from queue import Queue

class SkillProgressionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ap_gain = event.get('ap_gain')
            ent = event['ent']
            item = event.get('item')
            new_job = event.get('new_job')
            new_skill = event.get('new_skill')

            job = self.world.component_for_entity(ent, JobComponent).job
            sd_comp = self.world.component_for_entity(ent, SkillDirectoryComponent)                

            if item and new_skill:
                # Add this item's skill to the directory, if it is not already present.
                skill = None
                # TODO: This will change soon.
                for s in self.world.component_for_entity(item, SkillPoolComponent).skill_pool:
                    if s.is_active:
                        skill = s
                        break
                
                if skill and job.name in skill.job_req and skill not in sd_comp.skill_directory:
                    sd_comp.skill_directory.append(skill)

            elif ap_gain:
                # Go through each active skill and give them some AP.
                for skill in sd_comp.skill_directory:
                    if skill.is_active and not skill.is_mastered:
                        skill.ap += ap_gain
                        if skill.ap >= skill.ap_max:
                            skill.ap = skill.ap_max

                            self.world.messages.append({'skill_mastered': {'name': skill.name}})
                    
