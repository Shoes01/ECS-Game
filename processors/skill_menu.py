import esper

from _data import KEY_TO_SLOTS
from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.actor.skill_directory import SkillDirectoryComponent
from components.item.skill_pool import SkillPoolComponent
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
            new_job = event.get('new_job')
            skill_activate = event.get('skill_activate')
            skill_deactivate = event.get('skill_deactivate')
            skill_letter = event.get('skill_menu')

            equipped_items = self.world.component_for_entity(ent, EquipmentComponent).equipment
            sd_comp = self.world.component_for_entity(ent, SkillDirectoryComponent)

            # Create and display a menu of possible skills that may be activated.
            if skill_letter:
                slot = KEY_TO_SLOTS[skill_letter]

                mastered_list = []
                unmastered_list = []
                bestowed_list = [] # This should just be the one skill bestowed by the equipped item.

                # Populate mastered and unmastered lists.
                for skill in sd_comp.skill_directory:
                    if skill.is_mastered:
                        mastered_list.append(skill.name)
                    else:
                        unmastered_list.append(skill.name)
                
                # "Populate" the bestowed skill list.
                for item in equipped_items:
                    if self.world.component_for_entity(item, SlotComponent).slot == slot:
                        for skill in self.world.component_for_entity(item, SkillPoolComponent).skill_pool:
                            if self.world.component_for_entity(ent, JobComponent).job in skill.job_req:
                                bestowed_list.append(skill.name)

                menu = PopupMenu(title=f'Choose a {slot}-skill to equip.')
                
                for _list in (mastered_list, unmastered_list, bestowed_list):
                    for skill in _list:
                        _name = skill.name
                        _key = skill.name[0]
                        _processor = SkillMenuProcessor
                        _results = ( PopupChoiceResult(result={'ent': ent, 'skill_activate': skill}, processor=_processor),)
                        menu.contents.append(PopupChoice(name=_name, key=_key, results=_results))

                self.world.get_processor(StateProcessor).queue.put({'popup': menu})
            
            # Activate the chosen skill.
            elif skill_activate:
                new_skill = True

                for skill in sd_comp.skill_directory:
                    # Deactivate all skills for this slot.
                    if skill.slot == skill_activate.slot:
                        skill.is_active = False
                        # Except the chosen skill.
                        if skill.name == skill_activate.name:
                            skill.is_active = True
                            new_skill = False
                
                if new_skill:
                    skill_activate.is_active = True
                    sd_comp.skill_directory.append(skill_activate)

            elif skill_deactivate:
                # Deactivating all skills that belong to a slot is overkill, but this makes sure that one slot only ever has one skill active...
                for skill in sd_comp.skill_directory:
                    if skill.slot == skill_deactivate.slot:
                        skill.is_active = False
            
            elif new_job:
                # Jobs don't share skills, so it's safe to simply deactivate all unmastered jobs.
                for skill in sd_comp.skill_directory:
                    if not skill.is_mastered:
                        skill.is_active = False