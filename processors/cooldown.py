import esper

from components.actor.diary import CooldownEntry, DiaryComponent
from queue import Queue

class CooldownProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self.registered_entities = []
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event.get('ent')
            register_skill = event.get('register_skill')
            tick = event.get('tick')

            if register_skill:
                entry = CooldownEntry(remaining=register_skill.cooldown, skill=register_skill)
                self.world.component_for_entity(ent, DiaryComponent).cooldown.append(entry)

                if ent not in self.registered_entities:
                    self.registered_entities.append(ent)
            
            if tick:
                for ent in self.registered_entities:
                    diary = self.world.component_for_entity(ent, DiaryComponent)
                    remove_if = []

                    for entry in diary.cooldown:
                        entry.cooldown -= 1

                        if entry.cooldown <= 0:
                            remove_if.append(entry)

                    diary.remove(remove_if)

                    if not diary.cooldown:
                        self.registered_entities.remove(ent)
