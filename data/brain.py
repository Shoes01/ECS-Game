from collections import namedtuple

Brain = namedtuple('Brain', 'name')

NONE = Brain(name='none')
ZOMBIE = Brain(name='zombie')

all = {
    'NONE': NONE, 
    'ZOMBIE': ZOMBIE
}
