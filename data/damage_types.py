from collections import namedtuple

DamageType = namedtuple('DamageType', 'name')

NONE =      DamageType(name='none')
PHYSICAL =  DamageType(name='physical')
MAGICAL =   DamageType(name='magical')

all = {
    'NONE': NONE, 
    'PHTSICAL': PHYSICAL, 
    'MAGICAL': MAGICAL
}