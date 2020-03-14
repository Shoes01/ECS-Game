import attr

@attr.s(auto_attribs=True, slots=True)
class JobComponent:
    ' Component that stores the job of the entity, and its upkeep cost. '
    description: str
    name: str
    races: list
    skills: dict # Skills required to have to switch to this job ...
    upkeep: dict

    def update(self, job):
        self.description = job.description
        self.name = job.name
        self.races = job.races
        self.skills = job.skills
        self.upkeep = job.upkeep
