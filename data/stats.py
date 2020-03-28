HP = 'hp'
ATK = 'attack'
DEF = 'defense'
MAG = 'magic'
RES = 'resistance'
SPD = 'speed'

all = {
    'HP': HP,
    'ATK': ATK,
    'DEF': DEF,
    'MAG': MAG,
    'RES': RES,
    'SPD': SPD
}

from collections import namedtuple

Stats = namedtuple('Stats', 'stats')

# ACTORS ######################################################################
DEMON  = Stats(stats={ATK: 12, DEF: 15, HP: 100, MAG: 10, RES: 20, SPD: 10})
PLAYER = Stats(stats={ATK:  0, DEF:  1, HP:  10, MAG:  0, RES:  1, SPD:  2})
ZOMBIE = Stats(stats={ATK: 10, DEF:  3, HP:  20, MAG:  0, RES:  0, SPD:  0})
# FURNITURE ###################################################################
CHEST  = Stats(stats={ATK:  0, DEF:  0, HP:  10, MAG:  0, RES:  0, SPD:  0})
# ITEMS #######################################################################
HAMMER = Stats(stats={ATK:  7, DEF:  0, HP:   0, MAG:  0, RES:  0, SPD:  0})
SWORD  = Stats(stats={ATK:  5, DEF:  0, HP:   0, MAG:  0, RES:  0, SPD:  0})