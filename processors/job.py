import esper

from _helper_functions import generate_stats
from _jobs import JOBS, Job
from components.actor.job import JobComponent
from components.actor.race import RaceComponent
from components.actor.skill_directory import SkillDirectoryComponent
from processors.removable import RemovableProcessor
from processors.skill_directory import SkillDirectoryProcessor 
from processors.state import StateProcessor
from menu import PopupMenu, PopupChoice
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
                menu = PopupMenu(title='Which job would you like to adopt?')

                for _, job in JOBS.items():
                    _description = job.description
                    _name = job.name
                    _key = job.name[0]
                    _result = {'ent': ent, 'job': job}
                    _processor = JobProcessor
                    _upkeep = job.upkeep
                    _validity, _ = check_validity(ent, job, self.world)
                    
                    menu.contents.append(
                        PopupChoice(
                            name=_name, 
                            key=_key, 
                            result=_result, 
                            processor=_processor, 
                            valid=_validity, 
                            description=_description, 
                            upkeep=_upkeep
                        )
                    )
            
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            else:
                valid, message_data = check_validity(ent, job, self.world)
                
                if valid:
                    # Switch jobs!
                    ent_job = self.world.component_for_entity(ent, JobComponent)
                    ent_job.update_upkeep(job.upkeep)
                    ent_job.job = job.name
                    self.world.get_processor(SkillDirectoryProcessor).queue.put({'new_job': job.name, 'ent': ent})
                    self.world.get_processor(RemovableProcessor).queue.put({'new_job': job.name, 'ent': ent})
                
                self.world.messages.append({'job_switch': message_data})

def check_validity(ent, job, world):
    validity = True
    message_data = {}

    # Race validity.
    if world.component_for_entity(ent, RaceComponent).race not in job.races:
        validity = False
        message_data['wrong_race'] = True
    
    # Upkeep validity.
    ### The player may not switch to a job if it can't pay the upkeep. 
    ### However, other stats unrelated to the job may be negative.
    ### Note: _upkeep does not include the * -10.
    bare_stats = generate_stats(ent, world, include_upkeep=False)
    for key, value in job.upkeep.items():
        if bare_stats[key] - value * 10 < 0:
            validity = False
            message_data['not_enough_stats'] = True
    
    # Skill validity.
    sd_comp = world.component_for_entity(ent, SkillDirectoryComponent)
    for required_job, required_number in job.skills.items():
        # Determine how many skills from the given job have been mastered.
        mastery_number = 0
        if required_job in sd_comp.skill_directory:
            for name, ap in sd_comp.skill_directory[required_job].items():
                if ap[0] == ap[1]:
                    mastery_number += 1
            
        if mastery_number < required_number: 
            validity = False
            message_data['not_enough_skills'] = True

    if validity:
        message_data['switch_class'] = job.name

    return validity, message_data