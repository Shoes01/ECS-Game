from collections import namedtuple

Race = namedtuple('Race', 'name')

MONSTER =   Race(name='monster')
HUMAN =     Race(name='human')
ELF =       Race(name='elf')
KOBOLD =    Race(name='kobold')
ORC =       Race(name='orc')
GOBLIN =    Race(name='goblin')

all = {
    'MONSTER': MONSTER,
    'HUMAN': HUMAN,
    'ELF': ELF,
    'KOBOLD': KOBOLD,
    'ORC': ORC,
    'GOBLIN': GOBLIN
}
