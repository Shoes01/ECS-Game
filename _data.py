import tcod as libtcod

from collections import namedtuple

### CONSOLE DIMENSION DATA

Rectangle = namedtuple('Rectangle', ['x', 'y', 'w', 'h'])

border = 1

CON_W = 80
CON_H = 60
EQP_W = 12
EQP_H = 11

"""

con
+-----------+
|map        |
|           |
+---+-------+
|eqp|log    |
+---+-------+

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

LOG_COLORS = {
    'combat': libtcod.yellow,
    'death': libtcod.dark_red,
    'error': libtcod.red,
    'failure': libtcod.dark_red,
    'system_message': libtcod.dark_green,
    'success': libtcod.light_blue,
    'warning': libtcod.yellow
}

ENTITY_COLORS = {
    'corpse': libtcod.red,
    'player': libtcod.pink,
    'potion_heal': libtcod.red,
    'weapon': libtcod.blue,
    'zombie': libtcod.green
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