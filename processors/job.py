import esper

from _data import Jobs, Job
from _helper_functions import generate_stats
from components.actor.job import JobComponent
from components.actor.race import RaceComponent
from components.actor.skill_directory import SkillDirectoryComponent
from processors.removable import RemovableProcessor
from processors.skill_menu import SkillMenuProcessor
from processors.state import StateProcessor
from menu import PopupMenu, PopupChoice, PopupChoiceCondition, PopupChoiceResult
from queue import Queue

class JobProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            job = event.get('job')

            if not job:
                menu = PopupMenu(title='Which job would you like to adopt?', reveal_all=False)

                for _, job in Jobs.__dict__.items():
                    _description = job.description
                    _name = job.name
                    _key = job.name[0]
                    _result = {'ent': ent, 'job': job}
                    _processor = JobProcessor
                    _validity, _, _conditions = check_validity(ent, job, self.world)
                    
                    menu.contents.append(
                        PopupChoice(
                            name=_name, 
                            key=_key, 
                            results=(
                                PopupChoiceResult(
                                    result=_result, 
                                    processor=_processor
                                ),
                            ),
                            description=_description,
                            conditions=_conditions
                        )
                    )
            
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            else:
                valid, message_data, _ = check_validity(ent, job, self.world)
                
                if valid:
                    # Switch jobs!
                    ent_job = self.world.component_for_entity(ent, JobComponent)
                    ent_job.update_job(job)
                    self.world.get_processor(RemovableProcessor).queue.put({'ent': ent, 'new_job': job})
                    self.world.get_processor(SkillMenuProcessor).queue.put({'ent': ent, 'new_job': job})
                
                self.world.messages.append({'job_switch': message_data})

def check_validity(ent, job, world):
    conditions = []
    message_data = {}
    
    # Race validity.
    condition = PopupChoiceCondition(description=f"Your race needs to be one from {job.races}.")
    if world.component_for_entity(ent, RaceComponent).race not in job.races:
        condition.valid = False
        message_data['wrong_race'] = True
    conditions.append(condition)

    # Upkeep validity.
    ### The player may not switch to a job if it can't pay the upkeep. 
    ### However, other stats unrelated to the job may be negative.
    ### Note: _upkeep does not include the * -10.
    condition = PopupChoiceCondition(description=f"Your stats need to be at least {job.upkeep}.")
    bare_stats = generate_stats(ent, world, include_upkeep=False)
    for key, value in job.upkeep.items():
        if bare_stats[key] - value * 10 < 0:
            condition.valid = False
            message_data['not_enough_stats'] = True
    conditions.append(condition)
    
    # Skill validity.
    condition = PopupChoiceCondition(description=f"You need to have mastered at least skills like {job.skills}.")
    sd_comp = world.component_for_entity(ent, SkillDirectoryComponent)
    for required_job, required_number in job.skills.items():
        # Determine how many skills from the given job have been mastered.
        mastery_number = 0
        for skill in sd_comp.skill_directory:
            if skill.job_req == required_job and skill.is_mastered:
                mastery_number += 1
            
        if mastery_number < required_number: 
            condition.valid = False
            message_data['not_enough_skills'] = True
    conditions.append(condition)

    valid = True
    for condition in conditions:
        if condition.valid == False:
            valid = False
            break
    else:
        message_data['switch_class'] = job.name

    return valid, message_data, conditions