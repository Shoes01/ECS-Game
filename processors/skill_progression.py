import esper

from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.actor.skill_directory import SkillDirectoryComponent
from components.item.skills import SkillsComponent
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

            # First time check of the skill directory.
            if len(sd_comp.skill_directory) == 0:
                sd_comp.skill_directory[job.name] = {}

            # Add an entry to the ent's skill directory.
            if new_job:
                if new_job.name not in sd_comp.skill_directory.keys():
                    sd_comp.skill_directory[job] = {}

            elif item and new_skill:
                # Add this item's skill to the directory, if it is not already present.
                skill = None
                for s in self.world.component_for_entity(item, SkillsComponent).skills:
                    if s.active:
                        skill = s
                        break
                
                if skill and job in skill.job_req and job in sd_comp.skill_directory.keys():
                    if skill.name not in sd_comp.skill_directory[job].keys():
                        sd_comp.skill_directory[job][skill.name] = (0, skill.ap_max)
                    else:
                        print("ERROR: This item is trying to add a skill to a job that doesn't exist!")

            elif ap_gain:
                # Go through each item that is equipped, and add AP to its skill.
                eqp_comp = self.world.component_for_entity(ent, EquipmentComponent)
                for other_item in eqp_comp.equipment:
                    newly_maxed = False
                    other_skill = None 

                    # Get the skill, if there is one.
                    for s in self.world.component_for_entity(other_item, SkillsComponent).skills:
                        if s.active:
                            other_skill = s.name
                            break
                    else:
                        continue

                    ap_current, ap_max = sd_comp.skill_directory[job][other_skill]
                                        
                    already_maxed = True if ap_current == ap_max else False
                    
                    ap_current += ap_gain

                    if ap_current >= ap_max:
                        ap_current = ap_max
                        newly_maxed = True if not already_maxed else False

                    sd_comp.skill_directory[job][other_skill] = (ap_current, ap_max)

                    if newly_maxed:
                        message_data = {'name': other_skill}
                        self.world.messages.append({'skill_mastered': message_data})
