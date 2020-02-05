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

#############
### ENUMS ###
#############
import attr
from enum import Enum
from typing import List, Dict

# Slots
class SLOTS(Enum):
    HEAD = 'head'
    TORSO = 'torso'
    MAINHAND = 'mainhand'
    OFFHAND = 'offhand'
    FEET = 'feet'
    ACCESSORY = 'accessory'

# Races
class RACES(Enum):
    MONSTER = 'monster'
    HUMAN = 'human'
    ELF = 'elf'
    KOBOLD = 'kobold'
    ORC = 'orc'
    GOBLIN = 'goblin'

# AIs
class AI(Enum):
    ZOMBIE = 'zombie'

# Jobs
@attr.s(slots=True)
class Job:
    ' Data '
    description: str = attr.ib()
    name: str = attr.ib()
    ' Requirements '
    races: List[str] = attr.ib() # ['race',]
    skills: Dict[str, int] = attr.ib() # {'job': count}
    upkeep: Dict[str, int] = attr.ib() # {'stat': penalty value}

class JOBS(Enum):
    MONSTER = Job(
        description="Placeholder job for monsters.",
        name='monster job',
        races=(RACES.MONSTER,),
        skills={},
        upkeep={}
    )
    SOLDIER = Job(
        description="Baby's first job.",
        name='soldier', 
        races=(RACES.HUMAN,),
        skills={},
        upkeep={}
    )
    WARRIOR = Job(
        description='Has access to more devastating skills.', # Not rly.
        name='warrior',
        races=(RACES.HUMAN,),
        skills={},
        upkeep={'magic': 1, 'speed': 2}
    )
    BERSERKER = Job(
        description='Classic orc.',
        name='berserker',
        races=(RACES.ORC,),
        skills={},
        upkeep={'speed': 1, 'hp': 1}
    )
    ROGUE = Job(
        description='A job for seasoned fighters.',
        name='rogue',
        races=(RACES.HUMAN, RACES.GOBLIN, RACES.ELF),
        skills={'soldier': 1},
        upkeep={'speed': 1, 'hp': 15}
    )
    THIEF = Job(
        description='A stealer.',
        name='thief',
        races=(RACES.HUMAN,),
        skills={},
        upkeep={}
    )
# Rarities
@attr.s(slots=True, auto_attribs=True)
class Rarity:
    eccentricity: int # The greater the eccentricity, the greater the variation in base stats.
    name: str         # The name of this type of eccentricity.

class RARITY(Enum):
    AWFUL       = Rarity(eccentricity=-2, name="decayed")
    POOR        = Rarity(eccentricity=-1, name="hypobolic")
    COMMON      = Rarity(eccentricity= 0, name="circular")
    UNCOMMON    = Rarity(eccentricity= 1, name="elliptic")
    RARE        = Rarity(eccentricity= 3, name="parabolic")
    MYTHIC      = Rarity(eccentricity= 5, name="superbolic")
    GODLY       = Rarity(eccentricity= 9, name="hyperbolic")