import attr
import data.stats as Stats

@attr.s(auto_attribs=True, frozen=True, slots=True)
class JobComponent:
    ' Component that stores the job of the entity, and its upkeep cost. '
    description: str
    name: str
    races: list
    skills: dict = attr.Factory(dict) # Skills required to have to switch to this job ...
    upkeep: dict = {Stats.HP: 0, Stats.ATK: 0, Stats.DEF: 0, Stats.MAG: 0, Stats.RES: 0, Stats.SPD: 0}
