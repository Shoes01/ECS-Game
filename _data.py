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
    'heal': libtcod.light_blue,
    'max_hp': libtcod.light_blue
}