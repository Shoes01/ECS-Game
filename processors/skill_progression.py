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

            if ap_gain:
                # Go through each active skill and give them some AP.
                for skill in self.world.component_for_entity(ent, SkillDirectoryComponent).skill_directory:
                    if skill.is_active and not skill.is_mastered:
                        skill.ap += ap_gain
                        if skill.ap >= skill.ap_max:
                            skill.ap = skill.ap_max

                            self.world.messages.append({'skill_mastered': {'name': skill.name}})
                    
