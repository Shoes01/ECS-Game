import esper

from _helper_functions import generate_stats
from _jobs import JOBS, Job
from components.actor.job import JobComponent
from components.actor.race import RaceComponent
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
                    _name = job.name
                    _key = job.name[0]
                    _result = {'ent': ent, 'job': job}
                    _processor = JobProcessor

                    # /// Check the validity of the job change. ///
                    _validity = True
                    
                    # Race validity.
                    if self.world.component_for_entity(ent, RaceComponent).race not in job.races:
                        _validity = False
                    
                    # Upkeep validity.
                    ### The player may not switch to a job if it can't pay the upkeep. 
                    ### However, other stats unrelated to the job may be negative.
                    ### Note: job.upkeep does not include the * -10.
                    bare_stats = generate_stats(ent, self.world, include_upkeep=False)
                    for key, value in job.upkeep.items():
                        if bare_stats[key] - value * 10 < 0:
                            _validity = False

                    # /////////////////////////////////////////////
                    
                    menu.contents.append(PopupChoice(name=_name, key=_key, result=_result, processor=_processor, valid=_validity))
            
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            else:
                ent_job = self.world.component_for_entity(ent, JobComponent)
                ent_job.update_upkeep(job.upkeep)
                ent_job.job = job.name