import esper

from components.actor.diary import DiaryComponent
from components.actor.job import JobComponent
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
            skill_used = event.get('skill') # Use this? Maybe?

            diary = self.world.component_for_entity(ent, DiaryComponent)

            if ap_gain:
                # Go through each active skill and give them some AP.
                
                for entry in diary.mastery:
                    if entry.skill in diary.active:
                        entry.ap += ap_gain

                        if entry.skill == skill_used:
                            entry.ap += ap_gain
                        
                        if entry.ap >= entry.skill.ap_max:
                            entry.ap = entry.skill.ap_max
                            self.world.messages.append({'skill_mastered': {'name': entry.skill.name}})