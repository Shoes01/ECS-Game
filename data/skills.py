import data.damage_types as DamageTypes
import data.damage_types as Jobs
import data.races as Races
import data.stats as Stats

import numpy as np

class Skill:
    def __init__(self, ap_max, cooldown, cost_energy, cost_soul, damage_type, description, east, job_requirement, name, north_east):
        ' Skill Data. '
        self.ap_max = ap_max
        self.cooldown = cooldown
        self.cost_energy = cost_energy
        self.cost_soul = cost_soul
        self.damage_type = damage_type
        self.description = description
        self.job_requriement = job_requirement
        self.name = name
        self.slot = "This gets replaced by an actual slot when the item bestowing this skill is generated."

        ' Skill Directions. '
        self.east = np.array(east)
        self.north = np.rot90(self.east)
        self.west = np.rot90(self.north)
        self.south = np.rot90(self.west)
        self.north_east = np.array(north_east)
        self.north_west = np.rot90(self.north_east)
        self.south_west = np.rot90(self.north_west)
        self.south_east = np.rot90(self.south_west)


"""
The way skills interact with tiles are defined here.

1: Deal damage to this tile.",
2: Deal damage to this tile, BUT the skill will fail if there is a wall here.
3: Player ends in this tile, BUT the skill will fail if there is an actor here.
4: Nothing, BUT the skill will fail if there is an entity here.
"""
SPRINT = Skill(
    ap_max=100,
    cooldown=2,
    cost_energy=1,
    cost_soul={Stats.SPD: 2},
    damage_type=DamageTypes.NONE,
    description="Sprint to a safer location.",
    job_requirement=Jobs.ROGUE,
    name='sprint',
    east=
    [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 4, 3],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    north_east=
    [
        [0, 0, 0, 0, 3],
        [0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
)
FIRST_AID = Skill(
    ap_max=0,
    cooldown=3,
    cost_energy=0,
    cost_soul={Stats.SPD: 2, Stats.HP: -10, Stats.MAG: 2, Stats.DEF: 2, Stats.ATK: 2, Stats.DEF: 2},
    damage_type=DamageTypes.NONE,
    description='First aid, for your soul.',
    job_requirement=Jobs.SOLDIER,
    name='first aid',
    east=[
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],        
    north_east=[
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
)
LUNGE = Skill(
    ap_max=100,
    cooldown=5,
    cost_energy=2,
    cost_soul={Stats.MAG: 2},
    damage_type=DamageTypes.PHYSICAL,
    description='Lunge forward to strike a foe.',
    job_requirement=Jobs.SOLDIER,
    name='lunge',
    east=[
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],        
    north_east=[
        [0, 0, 0, 0, 2],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
)
CLEAVE = Skill(
    ap_max=100,
    cooldown=4,
    cost_energy=2,
    cost_soul={Stats.DEF: 5},
    damage_type=DamageTypes.PHYSICAL,
    description='A swinging strike.',
    job_requirement=Jobs.WARRIOR,
    name='cleave',
    east=[
        [0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0]
    ],        
    north_east=[
        [0, 0, 0, 0, 0],
        [0, 0, 2, 2, 0],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
)
HEADBUTT = Skill(
    ap_max=100,
    cooldown=3,
    cost_energy=1,
    cost_soul={Stats.HP: 1, Stats.RES: 4},
    damage_type=DamageTypes.PHYSICAL,
    description='Use your head for something.',
    job_requirement=Jobs.WARRIOR,
    name='headbutt',
    east=[
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],        
    north_east=[
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
)

all = {
    'SPRINT': SPRINT, 
    'FIRST_AID': FIRST_AID, 
    'LUNGE': LUNGE, 
    'HEADBUTT': HEADBUTT
}