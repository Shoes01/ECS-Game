from collections import namedtuple

DamageType = namedtuple('DamageType', 'name')

NONE =      DamageType(name='none')
HEAL =      DamageType(name='heal')
MAGICAL =   DamageType(name='magical')
PHYSICAL =  DamageType(name='physical')

all = {
    'NONE': NONE, 
    'HEAL': HEAL,
    'MAGICAL': MAGICAL,
    'PHTSICAL': PHYSICAL
}