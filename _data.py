from collections import namedtuple

### GAME MAP DATA

FINAL_FLOOR = 2
MULTIPLIER = 4
TICKS_PER_TURN = 1

### CONSOLE DIMENSION DATA

Rectangle = namedtuple('Rectangle', ['x', 'y', 'w', 'h'])

border = 1

CON_W = 60
CON_H = 40
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

### COLOR DATA
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
    'floor': COLOR_THEME['BrightGreen'],
    'floor_bg': COLOR_THEME['Green'],
    'floor_explored': COLOR_THEME['BrightBlack'],
    'mon_demon': COLOR_THEME['Red'],
    'mon_goblin': COLOR_THEME['Yellow'],
    'mon_orc': COLOR_THEME['Cyan'],
    'mon_rat': COLOR_THEME['BrightBlack'],
    'mon_kobold': COLOR_THEME['Blue'],
    'mon_zombie': COLOR_THEME['Green'],
    'overlap_bg': COLOR_THEME['BrightBlack'],
    'player': COLOR_THEME['BrightMagenta'],
    'potion_heal': COLOR_THEME['Red'],
    'skill_1': COLOR_THEME['BrightBlue'],
    'skill_2': COLOR_THEME['BrightBlue'],
    'skill_3': COLOR_THEME['BrightMagenta'],
    'skill_4': COLOR_THEME['Magenta'],
    'skill_blocked': COLOR_THEME['BrightRed'],
    'stairs': COLOR_THEME['White'],
    'stairs_explored': COLOR_THEME['BrightBlack'],
    'wall': COLOR_THEME['White'],
    'wall_bg': COLOR_THEME['Black'],
    'wall_explored': COLOR_THEME['BrightBlack'],
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
    'text_invalid': COLOR_THEME['White'],
    'text_mainmenu': COLOR_THEME['White']
}

### BORDER DATA

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