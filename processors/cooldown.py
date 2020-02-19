import esper

from components.actor.skill_directory import SkillDirectoryComponent
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
            remove_entity = event.get('remove_entity')
            tick = event.get('tick')

            if register_skill:
                for skill in self.world.component_for_entity(ent, SkillDirectoryComponent).skill_directory:
                    if skill.name == register_skill.name:
                        skill.cooldown_remaining = skill.cooldown

                self.registered_entities.append(ent)

            
            if remove_entity:
                self.registered_entities.remove(remove_entity)
                for skill in self.world.component_for_entity(remove_entity, SkillDirectoryComponent).skill_directory:
                    skill.cooldown_remaining = 0

            if tick:
                for ent in self.registered_entities:
                    all_cooled_down = True
                    
                    for skill in self.world.component_for_entity(ent, SkillDirectoryComponent).skill_directory:
                        if skill.cooldown_remaining:
                            skill.cooldown_remaining -= 1

                        if not skill.cooldown_remaining <= 0:
                            all_cooled_down = False

                    if all_cooled_down:
                        self.queue.put({'remove_entity': ent})
