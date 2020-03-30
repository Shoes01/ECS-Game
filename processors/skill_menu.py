import esper

from components.actor.diary import DiaryComponent, MasteryEntry
from components.actor.equipment import EquipmentComponent
from components.actor.job import JobComponent
from components.item.skill_pool import SkillPoolComponent
from components.item.slot import SlotComponent
from data.components_master import SLOTS
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
            diary = self.world.component_for_entity(ent, DiaryComponent)

            # Create and display a menu of possible skills that may be activated.
            if skill_letter:
                slot = SLOTS._key_to_slots[skill_letter]

                mastered_list = []
                unmastered_list = []
                bestowed_list = [] # This should just be the one skill bestowed by the equipped item.

                # Populate mastered and unmastered lists.
                for entry in diary.mastery:
                    if entry.skill.ap_max == entry.ap:
                        mastered_list.append(entry.skill)
                    else:
                        unmastered_list.append(entry.skill)
                
                # "Populate" the bestowed skill list.
                for item in equipped_items:
                    if self.world.component_for_entity(item, SlotComponent) == slot:
                        for skill in self.world.component_for_entity(item, SkillPoolComponent).skill_pool:
                            print(f"Skill: {skill.name}.\nFirst: {self.world.component_for_entity(ent, JobComponent) == skill.job_req}. Second: {skill not in mastered_list}")
                            if self.world.component_for_entity(ent, JobComponent) == skill.job_req and skill not in mastered_list:
                                bestowed_list.append(skill)

                menu = PopupMenu(title=f'Choose a {slot.name}-skill to equip.')
                
                for _list in (mastered_list, unmastered_list, bestowed_list):
                    for skill in _list:
                        _name = skill.name
                        _key = skill.name[0]
                        _processor = SkillMenuProcessor
                        _results = ( PopupChoiceResult(result={'ent': ent, 'skill_activate': skill}, processor=_processor),)
                        menu.contents.append(PopupChoice(name=_name, key=_key, results=_results))

                self.world.get_processor(StateProcessor).queue.put({'popup': menu})
            
            # Activate the chosen skill. Deactivate the skill that the chosen one is replacing.
            elif skill_activate:
                skill_deactivate = None

                for skill in diary.active:
                    if skill.slot == skill_activate.slot:
                        skill_deactivate = skill
                        break

                if skill_deactivate:
                    diary.active.remove(skill_deactivate)
                
                diary.active.append(skill_activate)

                # Track the mastery of the skill, if we're not already doing that.
                for entry in diary.mastery:
                    if entry.skill == skill_activate:
                        break
                else:
                    diary.mastery.append(MasteryEntry(skill=skill_activate, ap=0))

            elif skill_deactivate:
                # Deactivating all skills that belong to a slot is overkill, but this makes sure that one slot only ever has one skill active...
                diary.active.remove(skill_deactivate)
            
            elif new_job:
                # Jobs don't share skills, so it's safe to simply deactivate all unmastered jobs.
                for entry in diary.mastery:
                    if entry.skill in diary.active and entry.ap != entry.skill.ap_max:
                        diary.active.remove(entry.skill)