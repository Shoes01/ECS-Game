import esper

from components.item.skill import ItemSkillComponent
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
                skill_comp = self.world.component_for_entity(register_item, ItemSkillComponent)
                skill_comp.cooldown_remaining = skill_comp.cooldown
                self.registered_items.append(register_item)
            
            if remove_item:
                self.registered_items.remove(remove_item)

            if tick:
                for item in self.registered_items:
                    skill_comp = self.world.component_for_entity(item, ItemSkillComponent)
                    
                    skill_comp.cooldown_remaining -= 1

                    if skill_comp.cooldown_remaining <= 0:
                        self.queue.put({'remove': item})