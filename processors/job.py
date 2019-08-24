import esper

from _jobs import JOBS, Job
from components.actor.job import JobComponent
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

                for key, job in JOBS.items():
                    _name = job.name
                    _key = job.name[0]
                    _result = {'ent': ent, 'job': job}
                    _processor = JobProcessor
                    menu.contents.append(PopupChoice(name=_name, key=_key, result=_result, processor=_processor))
            
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            else:
                ent_job = self.world.component_for_entity(ent, JobComponent)
                ent_job.update_upkeep(job.upkeep)
                ent_job.job = job.name