import esper

from components.item.skills import SkillPoolComponent
from queue import Queue

class CooldownProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self.registered_items = []
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            register_item = event.get('register')
            remove_item = event.get('remove')
            tick = event.get('tick')

            if register_item:
                for skill in self.world.component_for_entity(register_item, SkillPoolComponent).skill_pool:
                    if skill.active:
                        skill.cooldown_remaining = skill.cooldown
                self.registered_items.append(register_item)
            
            if remove_item:
                self.registered_items.remove(remove_item)

            if tick:
                for item in self.registered_items:
                    for skill in self.world.component_for_entity(register_item, SkillPoolComponent).skill_pool:
                        if skill.active:
                            skill.cooldown_remaining -= 1
                    
                        if skill.cooldown_remaining <= 0:
                            self.queue.put({'remove': item})