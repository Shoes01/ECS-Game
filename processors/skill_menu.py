import esper

from _data import KEY_TO_SLOTS
from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.actor.skill_directory import SkillDirectoryComponent
from components.item.skills import SkillsComponent, SkillComponent
from components.item.slot import SlotComponent
from processors.state import StateProcessor
from menu import PopupMenu, PopupChoice, PopupChoiceResult, PopupChoiceCondition
from queue import Queue

class SkillMenuProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            skill_letter = event['skill_menu']

            slot = KEY_TO_SLOTS[skill_letter]

            entire_skill_list = self.world.table_slot_skill[slot] # This is the full list of possible skills for this slot.
            equipped_items = self.world.component_for_entity(ent, EquipmentComponent).equipment
            skill_directory = self.world.component_for_entity(ent, SkillDirectoryComponent).skill_directory

            mastered_list = []
            unmastered_list = []
            bestowed_list = [] # This should just be the one skill bestowed by the equipped item.

            # Populate mastered and unmastered lists.
            for _job, skill in skill_directory.items():
                for name, AP in skill.items():
                    if name in entire_skill_list:
                        if AP[0] == AP[1]:
                            mastered_list.append(name)
                        else:
                            unmastered_list.append(name)
            
            # Need to also add the skill that the currently equipped skill is bestowing.
            for item in equipped_items:
                if self.world.has_component(item, SkillsComponent) and self.world.component_for_entity(item, SlotComponent).slot == slot:
                    skills = self.world.component_for_entity(item, SkillsComponent).skills
                    for skill in skills:
                        if self.world.component_for_entity(ent, JobComponent).job in skill.job_req:
                            bestowed_list.append(skill.name)

            menu = PopupMenu(title=f'Choose a {slot}-skill to equip.')

            n = 97
            for _list in (mastered_list, unmastered_list, bestowed_list):
                for skill in _list:
                    _name = skill
                    _key = chr(n)
                    _processor = self # Just for an initial test...
                    _results = ( PopupChoiceResult(result={'ent': ent}, processor=_processor),)
                    menu.contents.append(PopupChoice(name=_name, key=_key, results=_results))
                    n += 1

            self.world.get_processor(StateProcessor).queue.put({'popup': menu})

