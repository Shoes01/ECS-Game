import attr
import data.races as Races

from typing import Dict, List

@attr.s(auto_attribs=True, slots=True)
class Job:
    ' Data '
    description: str
    name: str
    ' Requirements '
    races: List[str]        # ['race',]
    skills: Dict[str, int]  # {'job': count}
    upkeep: Dict[str, int]  # {'stat': penalty value}

MONSTER = Job(
    description="Placeholder job for monsters.",
    name='monster job',
    races=(Races.MONSTER,),
    skills={},
    upkeep={}
)
SOLDIER = Job(
    description="Baby's first job.",
    name='soldier', 
    races=(Races.HUMAN,),
    skills={},
    upkeep={}
)
WARRIOR = Job(
    description='Has access to more devastating skills.', # Not rly.
    name='warrior',
    races=(Races.HUMAN,),
    skills={},
    upkeep={'magic': 1, 'speed': 2}
)
BERSERKER = Job(
    description='Classic orc.',
    name='berserker',
    races=(Races.ORC,),
    skills={},
    upkeep={'speed': 1, 'hp': 1}
)
ROGUE = Job(
    description='A job for seasoned fighters.',
    name='rogue',
    races=(Races.HUMAN, Races.GOBLIN, Races.ELF),
    skills={'soldier': 1},
    upkeep={'speed': 1, 'hp': 15}
)
THIEF = Job(
    description='A stealer.',
    name='thief',
    races=(Races.HUMAN,),
    skills={},
    upkeep={}
)

all = {
    'MONSTER': MONSTER, 
    'SOLDIER': SOLDIER, 
    'WARRIOR': WARRIOR, 
    'BERSERKER': BERSERKER, 
    'ROGUE': ROGUE, 
    'THIEF': THIEF
}
