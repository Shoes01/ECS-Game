import attr

@attr.s(auto_attribs=True, slots=True)
class JobComponent:
    ' Component that stores the job of the entity, and its upkeep cost. '
    description: str
    name: str
    races: list
    skills: dict = attr.Factory(dict) # Skills required to have to switch to this job ...
    upkeep: dict = attr.Factory(dict) 
