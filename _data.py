from collections import namedtuple

#####################
### GAME MAP DATA ###
#####################

FINAL_FLOOR = 2
FONTSHEET = 'Zaratustra-msx.png'
FONTSIZE = 8
FOV_RADIUS = 5
MULTIPLIER = 4
TICKS_PER_TURN = 1

##############################
### CONSOLE DIMENSION DATA ###
##############################

Rectangle = namedtuple('Rectangle', ['x', 'y', 'w', 'h'])

border = 1

CON_W = 120
CON_H = 80
EQP_W = 20
EQP_H = 12

"""

con
+-----------+
|map        |
|           |
+----+------+
|eqp |log   |
+----+------+

"""

con = Rectangle(
    x=0,
    y=0,
    w=CON_W,
    h=CON_H
)

eqp = Rectangle(
    x=border,
    y=CON_H - border - EQP_H,
    w=EQP_W,
    h=EQP_H
)

map = Rectangle(
    x=border,
    y=border,
    w=CON_W - 2*border,
    h=CON_H - 3*border - EQP_H
)

log = Rectangle(
    x=2*border + EQP_W,
    y=CON_H - border - EQP_H,
    w=CON_W - 3*border - EQP_W,
    h=EQP_H
)

##################
### COLOR DATA ###
##################

"""
# FrontEndDelight Theme
COLOR_THEME = {
    "Black": (36,36,38),
    "Blue": (44,112,183),
    "BrightBlack": (94,172,108),
    "BrightBlue": (51,147,201),
    "BrightCyan": (78,188,229),
    "BrightGreen": (116,235,76),
    "BrightMagenta": (231,94,78),
    "BrightRed": (246,67,25),
    "BrightWhite": (139,115,90),
    "BrightYellow": (252,194,36),
    "Cyan": (59,160,165),
    "Green": (86,87,70),
    "Magenta": (240,45,78),
    "Red": (248,80,26),
    "White": (172,172,172),
    "Yellow": (249,118,29),
    "Background": (27,27,29)
}
"""
# ENCOM Color Theme
COLOR_THEME = {
    "Black": (36,36,38),
    "Blue": (0,129,255),
    "BrightBlack": (84,84,84),
    "BrightBlue": (0,0,255),
    "BrightCyan": (0,205,205),
    "BrightGreen": (0,238,0),
    "BrightMagenta": (255,0,255),
    "BrightRed": (255,0,0),
    "BrightWhite": (255, 255, 255),
    "BrightYellow": (255, 255, 0),
    "Cyan": (0,139,139),
    "Green": (0,139,0),
    "Magenta": (188,0,202),
    "Red": (159,0,0),
    "White": (187,187,187),
    "Yellow": (255,207,0),
    "Background": (0, 0, 0)
}

ENTITY_COLORS = {
    'armor': COLOR_THEME['Magenta'],
    'chest': COLOR_THEME['Yellow'],
    'con_jar': COLOR_THEME['BrightCyan'],
    'corpse': COLOR_THEME['BrightRed'],
    'floor': COLOR_THEME['BrightWhite'],
    'floor_bg': COLOR_THEME['BrightBlack'],
    'floor_explored': COLOR_THEME['Background'],
    'loot_plural_fg': COLOR_THEME['Yellow'],
    'loot_plural_bg': COLOR_THEME['BrightYellow'],
    'mon_demon': COLOR_THEME['Red'],
    'mon_goblin': COLOR_THEME['Yellow'],
    'mon_orc': COLOR_THEME['Cyan'],
    'mon_rat': COLOR_THEME['Green'],
    'mon_kobold': COLOR_THEME['Blue'],
    'mon_zombie': COLOR_THEME['BrightGreen'],
    'overlap_bg': COLOR_THEME['BrightCyan'],
    'player': (50, 100, 100, 'hsv'), #COLOR_THEME['BrightMagenta'],
    'potion_heal': COLOR_THEME['Red'],
    'skill_1': COLOR_THEME['BrightBlue'],
    'skill_2': COLOR_THEME['BrightBlue'],
    'skill_3': COLOR_THEME['BrightMagenta'],
    'skill_4': COLOR_THEME['Magenta'],
    'skill_blocked': COLOR_THEME['BrightRed'],
    'stairs': COLOR_THEME['White'],
    'stairs_bg': COLOR_THEME['BrightBlack'],
    'stairs_explored': COLOR_THEME['Background'],
    'wall': COLOR_THEME['White'],
    'wall_bg': COLOR_THEME['BrightBlack'],
    'wall_explored': COLOR_THEME['Background'],
    'weapon': COLOR_THEME['Blue']
}

LOG_COLORS = {
    'combat': COLOR_THEME['Yellow'],
    'death': COLOR_THEME['Red'],
    'error': COLOR_THEME['BrightRed'],
    'failure': COLOR_THEME['Red'],
    'skill': COLOR_THEME['BrightGreen'],
    'system_message': COLOR_THEME['Green'],
    'success': COLOR_THEME['Blue'],
    'warning': COLOR_THEME['BrightYellow']
}

UI_COLORS = {
    'border_main': COLOR_THEME['BrightWhite'],
    'border_secondary': COLOR_THEME['White'],
    'cooldown': COLOR_THEME['Red'],
    'cursor': COLOR_THEME['Yellow'],
    'bg': COLOR_THEME['Black'],
    'fg': COLOR_THEME['BrightWhite'],
    'text': COLOR_THEME['BrightWhite'],
    'text_condition_unmet': COLOR_THEME['Red'],
    'text_invalid': COLOR_THEME['White'],
    'text_mainmenu': COLOR_THEME['White']
}

###################
### SPRITE DATA ###
###################

SPRITES = {
    'blank': 0,
    'corpse': 480,
    'player': 126,
    # Entities defined in consumables.json
    'con_soul_jar': 818,
    # Entities defined in equipment.json
    'eqp_boots': 744,
    'eqp_dagger': 896,
    'eqp_hammer': 933,
    'eqp_hammer_war': 966,
    'eqp_helmet': 705,
    'eqp_shield': 837,
    'eqp_sword': 898,
    'eqp_sword_great': 964,
    'eqp_sword_long': 928,
    # Entities defined in monsters.json
    'mon_demon': 191,
    'mon_goblin': 89,
    'mon_kobold': 314,
    'mon_orc': 91,
    'mon_rat': 287,
    'mon_zombie': 25,
    # Entities defined in other.json
    'other_chest': 388,
    # Entities defined in tiles.json
    'floor_stone': 51,
    'stairs': 195,
    'wall_stone': 554,
    'wall_stone_var_1': 555,
    'wall_stone_var_2': 556, 
    'wall_stone_var_3': 557,
    'wall_stone_topleft': 18,
    'wall_stone_top': 19,
    'wall_stone_topright': 20,
    'wall_stone_left': 50,
    'wall_stone_right': 52,
    'wall_stone_bottomleft': 82,
    'wall_stone_bottom': 83,
    'wall_stone_bottomright': 84,
    # None json defined entities
    'loot_plural': 200
}

###################
### BORDER DATA ###
###################

class DoubleLineBox():
    horizontal = u'\u2550' # ═
    vertical = u'\u2551' # ║
    top_left = u'\u2554' # ╔
    top_right = u'\u2557' # ╗
    bottom_left = u'\u255a' # ╚
    bottom_right = u'\u255d' # ╝
    not_left = u'\u2560' # ╠
    not_right = u'\u2563' # ╣
    not_up = u'\u2566' # ╦
    not_down = u'\u2569' # ╩
    intersection = u'\u256c' # ╬
    wse_special = u'\u2564' # ╤
    nws_special = u'\u2567' # ╧
    left_bookend = u'\u2561' # ╡
    right_bookend = u'\u255e' # ╞

class SingleLineBox():
    vertical = u'\u2502' # │
    horizontal = u'\u2500' # ─
    top_left = u'\u250c' # ┌
    top_right = u'\u2510' # ┐
    bottom_left = u'\u2514' # └
    bottom_right = u'\u2518' # ┘
    not_left = u'\u251c' # ├
    not_up = u'\u252c' # ┬
    not_down = u'\u2534' # ┴
    intersection = u'\u253c' # ┼

#################
### CONSTANTS ###
#################
import attr
from typing import List, Dict

# Slots
@attr.s(auto_attribs=True)
class Slots():
    HEAD: str = 'head'          # w
    TORSO: str = 'torso'        # s
    MAINHAND: str = 'mainhand'  # q
    OFFHAND: str = 'offhand'    # a
    FEET: str = 'feet'          # d
    ACCESSORY: str = 'accessory' # e

Slots = Slots()

SLOTS_TO_KEY = {
    Slots.HEAD: 'w',
    Slots.TORSO: 's',
    Slots.MAINHAND: 'q',
    Slots.OFFHAND: 'a',
    Slots.FEET: 'd',
    Slots.ACCESSORY: 'e'
}

KEY_TO_SLOTS = {
    'w': Slots.HEAD,
    's': Slots.TORSO,
    'q': Slots.MAINHAND,
    'a': Slots.OFFHAND,
    'd': Slots.FEET,
    'e': Slots.ACCESSORY
}

# Races
@attr.s(auto_attribs=True)
class Races:
    MONSTER: str = 'monster'
    HUMAN: str = 'human'
    ELF: str = 'elf'
    KOBOLD: str = 'kobold'
    ORC: str = 'orc'
    GOBLIN: str = 'goblin'

Races = Races()

# AIs
@attr.s(auto_attribs=True)
class AI_:
    ZOMBIE: str = 'zombie'

AI = AI_()

# Jobs
@attr.s(auto_attribs=True, slots=True)
class Job:
    ' Data '
    description: str
    name: str
    ' Requirements '
    races: List[str]        # ['race',]
    skills: Dict[str, int]  # {'job': count}
    upkeep: Dict[str, int]  # {'stat': penalty value}

@attr.s(auto_attribs=True)
class Jobs:
    MONSTER: Job = Job(
        description="Placeholder job for monsters.",
        name='monster job',
        races=(Races.MONSTER,),
        skills={},
        upkeep={}
    )
    SOLDIER: Job = Job(
        description="Baby's first job.",
        name='soldier', 
        races=(Races.HUMAN,),
        skills={},
        upkeep={}
    )
    WARRIOR: Job = Job(
        description='Has access to more devastating skills.', # Not rly.
        name='warrior',
        races=(Races.HUMAN,),
        skills={},
        upkeep={'magic': 1, 'speed': 2}
    )
    BERSERKER: Job = Job(
        description='Classic orc.',
        name='berserker',
        races=(Races.ORC,),
        skills={},
        upkeep={'speed': 1, 'hp': 1}
    )
    ROGUE: Job = Job(
        description='A job for seasoned fighters.',
        name='rogue',
        races=(Races.HUMAN, Races.GOBLIN, Races.ELF),
        skills={'soldier': 1},
        upkeep={'speed': 1, 'hp': 15}
    )
    THIEF: Job = Job(
        description='A stealer.',
        name='thief',
        races=(Races.HUMAN,),
        skills={},
        upkeep={}
    )

Jobs = Jobs()

# Rarities
@attr.s(auto_attribs=True, slots=True)
class Rarity:
    eccentricity: int # The greater the eccentricity, the greater the variation in base stats.
    name: str         # The name of this type of eccentricity.
    rank: int         # The rank of the rarity. 0 is lowest.

@attr.s(auto_attribs=True)
class Rarities:
    AWFUL: Rarity       = Rarity(eccentricity=-2, name="decayed",    rank=0)
    POOR: Rarity        = Rarity(eccentricity=-1, name="hypobolic",  rank=1)
    COMMON: Rarity      = Rarity(eccentricity= 0, name="circular",   rank=2)
    UNCOMMON: Rarity    = Rarity(eccentricity= 1, name="elliptic",   rank=3)
    EPIC: Rarity        = Rarity(eccentricity= 3, name="parabolic",  rank=4)
    RARE: Rarity        = Rarity(eccentricity= 5, name="superbolic", rank=5)
    MYTHIC: Rarity      = Rarity(eccentricity= 9, name="hyperbolic", rank=6)

Rarities = Rarities()

# Stats
@attr.s(auto_attribs=True)
class Stats:
    HP: str = 'hp'
    ATK: str = 'attack'
    DEF: str = 'defense'
    MAG: str = 'magic'
    RES: str = 'resistance'
    SPD: str = 'speed'

Stats = Stats()

# Damage Types
@attr.s(auto_attribs=True, slots=True)
class DamageType:
    NONE: str = "none"
    PHYSICAL: str = "physical"
    MAGICAL: str = "magical"

DamageType = DamageTypes()

# Skills
@attr.s(auto_attribs=True, slots=True)
class Skill:
    ap_max: int
    cooldown: int
    cost_energy: int # How many turns it takes to use the skill.
    cost_soul: dict # How much this skill takes from stats.
    description: str
    job_requriement: list # List of Jobs.
    east: Any # A numpy array.. oof
    north_east: Any # Another numpy array.

@attr.s(auto_attribs=True, slots=True)
class Skills:
    """
    The way skills interact with tiles are defined here.

    1: Deal damage to this tile.",
    2: Deal damage to this tile, BUT the skill will fail if there is a wall here.
    3: Player ends in this tile, BUT the skill will fail if there is an actor here.
    4: Nothing, BUT the skill will fail if there is an entity here.
    """
    SPRINT: Skill = Skill(
        ap_max=100,
        cooldown=2,
        cost_energy=1,
        cost_soul={Stats.SPD: 2},
        damage_type=DamageType.NONE,
        description="Sprint to a safer location.",
        job_requirement=Jobs.ROGUE
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
    FIRST_AID: Skill = Skill(
        ap_max=0,
        cooldown=3,
        cost_energy=0,
        cost_soul={Stats.SPD: 2, Stats.HP: -10, Stats.MAG: 2, Stats.DEF: 2, Stats.ATK: 2, Stats.DEF: 2}
        damage_type=DamageType.NONE,
        description='First aid, for your soul.',
        job_requirement=Jobs.SOLDIER,
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
    LUNGE: Skill = Skill(
        ap_max=100,
        cooldown=5,
        cost_energy=2,
        cost_soul={Stats.MAG: 2}
        damage_type=DamageType.PHYSICAL,
        description='Lunge forward to strike a foe.',
        job_requirement=Jobs.SOLDIER,
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
    CLEAVE: Skill = Skill(
        ap_max=100,
        cooldown=4,
        cost_energy=2,
        cost_soul={Stats.DEF: 5}
        damage_type=DamageType.PHYSICAL,
        description='A swinging strike.',
        job_requirement=Jobs.WARRIOR,
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
    HEADBUTT: Skill = Skill(
        ap_max=100,
        cooldown=3,
        cost_energy=1,
        cost_soul={Stats.HP: 1, Stats.RES: 4}
        damage_type=DamageType.PHYSICAL,
        description='Use your head for something.',
        job_requirement=Jobs.WARRIOR,
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

    Skills = Skills()