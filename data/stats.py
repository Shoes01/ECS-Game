HP = 'hp'
ATK = 'attack'
DEF = 'defense'
MAG = 'magic'
RES = 'resistance'
SPD = 'speed'

all = {
    'HP': HP,
    'ARK': ATK,
    'DEF': DEF,
    'MAG': MAG,
    'RES': RES,
    'SPD': SPD
}

# ACTORS ######################################################################
DEMON  = {ATK: 12, DEF: 15, HP: 100, MAG: 10, RES: 20, SPD: 10}
PLAYER = {ATK:  5, DEF:  5, HP:  10, MAG:  5, RES:  5, SPD:  5}
ZOMBIE = {ATK:  3, DEF:  1, HP:   0, MAG:  0, RES:  0, SPD:  0}
# FURNITURE ###################################################################
CHEST  = {ATK:  0, DEF:  0, HP:  10, MAG:  0, RES:  0, SPD:  0}