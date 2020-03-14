from collections import namedtuple

Brain = namedtuple('Brain', 'awake name')

NONE = Brain(awake=False, name='none')
ZOMBIE = Brain(awake=False, name='zombie')

all = {
    'NONE': NONE, 
    'ZOMBIE': ZOMBIE
}
