import attr

@attr.s(auto_attribs=True, slots=True)
class Render:
    char: str
    color_fg: str
    codepoint: str

##################
### CHARACTERS ###
##################

" I won't be putting anything here, as I will be using sprites ... this is legacy stuff? lol. "

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

##################
### CODEPOINTS ###
##################

SPRITES = {
    'blank': 0,
    'corpse': 480,
    'player': 126,
    # Entities defined in consumables.json
    'con_soul_jar': 818,
    # Used in data/equipment.py
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
