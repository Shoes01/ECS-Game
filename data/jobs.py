from collections import namedtuple

import data.races as Races
import data.stats as Stats

Job = namedtuple('Job', 'description name races skills upkeep', defaults=({}, {}))
# Description: Describes the job.
# Name: The name of the job.
# Races: List of races capable of doing this job.
# Skills: Number of skills required to do this job.
# Upkeep: Stats required to do this job.

# TIER 0 ######################################################################
MONSTER = Job(
    description= "Placeholder job for monsters.",
    name= 'monster job',
    races= (Races.MONSTER,)
)
BERSERKER = Job(
    description= 'Classic orc.',
    name= 'berserker',
    races= (Races.ORC,),
    skills= {},
    upkeep= {Stats.SPD: 1, Stats.HP: 1}
)
SOLDIER = Job(
    description= "Baby's first job.",
    name= 'soldier', 
    races= (Races.HUMAN,)
)
THIEF = Job(
    description= 'A stealer.',
    name= 'thief',
    races= (Races.HUMAN,)
)
WARRIOR = Job(
    description= 'Has access to more devastating skills.', # Not rly.
    name= 'warrior',
    races= (Races.HUMAN,),
    skills= {},
    upkeep= {Stats.MAG: 1, Stats.SPD: 2}
)

# TIER 1 ######################################################################
ROGUE = Job(
    description= 'A job for seasoned fighters.',
    name= 'rogue',
    races= (Races.HUMAN, Races.GOBLIN, Races.ELF),
    skills= {SOLDIER: 1},
    upkeep= {Stats.ATK: 1, Stats.HP: 15}
)

all = {
    'MONSTER': MONSTER, 
    'SOLDIER': SOLDIER, 
    'WARRIOR': WARRIOR, 
    'BERSERKER': BERSERKER, 
    'ROGUE': ROGUE, 
    'THIEF': THIEF
}
