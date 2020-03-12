import attr

@attr.s(auto_attribs=True, slots=True)
class JobComponent:
    description: str
    name: str
    races: list
    skills: dict # Skills required to have to switch to this job ...
    upkeep: dict



# TODO: The logic here should be moved into the processor...

import data.jobs as Jobs
import data.stats as Stats

class JobComponent:
    ' Component that stores the job of the entity, and its upkeep cost. '
    __slots__ = 'job', 'upkeep'
    def __init__(self, job):
        
        self.job = job
        self.upkeep = job.upkeep
        
        self.update_upkeep(self.upkeep)
    
    def update_job(self, JOB):
        self.job = JOB
        self.update_upkeep(JOB.upkeep)        

    def update_upkeep(self, upkeep):
        new_upkeep = {
            Stats.HP:  0,
            Stats.ATK: 0,
            Stats.MAG: 0,
            Stats.SPD: 0,
            Stats.DEF: 0,
            Stats.RES: 0
        }
        
        for stat, value in upkeep.items():
            new_upkeep[stat] = -10 * value # Negative because substracting dicts is hard; x10 because of the decimal display.
        
        self.upkeep = new_upkeep