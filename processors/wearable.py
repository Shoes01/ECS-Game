import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.job import JobComponent
from components.item.jobreq import JobReqComponent
from components.item.skills import SkillsComponent
from components.item.slot import SlotComponent
from components.item.wearable import WearableComponent
from components.name import NameComponent
from menu import PopupMenu, PopupChoice, PopupChoiceResult
from processors.energy import EnergyProcessor
from processors.removable import RemovableProcessor
from processors.skill import SkillProcessor
from processors.skill_progression import SkillProgressionProcessor
from processors.state import StateProcessor
from queue import Queue

class WearableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            item = event.get('item')

            eqp = self.world.component_for_entity(ent, EquipmentComponent)

            if not item:
                # Create popup menu for player to choose from.
                menu = PopupMenu(title='Which item would you like to wear or remove?')
                
                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory:
                    if not self.world.has_component(item, WearableComponent):
                        continue
                    _name = self.world.component_for_entity(item, NameComponent).name
                    _key = chr(n)
                    _results = (PopupChoiceResult(result={'ent': ent, 'item': item}, processor=WearableProcessor),)
                    menu.contents.append(PopupChoice(name=_name, key=_key, results=_results))
                    n += 1
                
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            else:
                # Wear the item.
                name_component = self.world.component_for_entity(item, NameComponent)
                turn = self.world.turn
                slot_filled_item = None
                
                # Check to see that the entity is not already wearing an item in the slot.
                slot_filled = False
                for worn_item in eqp.equipment:
                    if self.world.component_for_entity(worn_item, SlotComponent).slot == self.world.component_for_entity(item, SlotComponent).slot:
                        slot_filled = True
                        slot_filled_item = worn_item
                        break

                # Prepare message log data.
                message_data = {
                    'name': name_component.name,
                    'slot': self.world.component_for_entity(item, SlotComponent).slot,
                    'turn': turn
                }

                if item in eqp.equipment:
                    # Already worn, so remove it.
                    message_data = {} # Clear the message data, as the RemovableProcessor will do its own thing.
                    self.world.get_processor(RemovableProcessor).queue.put({'ent': ent, 'item': item})
                elif slot_filled:
                    # An item is already in the slot we want; swap the two items.
                    # Wear the item!
                    wear_item(ent, eqp, item, name_component, self.world)
                    message_data['success'] = 'slot_filled'
                    # Remove the other item.
                    self.world.get_processor(RemovableProcessor).queue.put({'ent': ent, 'item': slot_filled_item})
                elif self.world.component_for_entity(ent, JobComponent).job not in self.world.component_for_entity(item, JobReqComponent).job_req:
                    # Not the correct job to wear the item.
                    message_data['success'] = 'wrong_job'
                    message_data['job'] = self.world.component_for_entity(item, JobReqComponent).job_req
                elif self.world.has_component(item, WearableComponent):
                    # Wear the item!
                    wear_item(ent, eqp, item, name_component, self.world)
                    message_data['success'] = True
                else:
                    # This is not a wearable item.
                    message_data['success'] = False
                
                self.world.messages.append({'wear': message_data})

def wear_item(ent, eqp, item, name_component, world):
    name_component.name += ' (worn)'
    eqp.equipment.append(item)
    world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'item': True})
    world.get_processor(SkillProgressionProcessor).queue.put({'ent': ent, 'item': item, 'new_skill': True})
    
    # Go through the skills of the item and deactivate those that don't meet the job_requirement.
    job = world.component_for_entity(ent, JobComponent).job
    for skill in world.component_for_entity(item, SkillsComponent).skills:
        if job in skill.job_req:
            skill.active = True
        else:
            skill.active = False
