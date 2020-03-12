from collections import namedtuple

Slot = namedtuple('Slot', 'name key')

HEAD =      Slot(name='head',        key='w')
TORSO =     Slot(name='torso',       key='s')
MAINHAND =  Slot(name='mainhand',    key='q')
OFFHAND =   Slot(name='offhand',     key='a')
FEET =      Slot(name='feet',        key='d')
ACCESSORY = Slot(name='accessory',   key='e')

all = {
    'HEAD': HEAD,
    'TORSO': TORSO,
    'MAINHAND': MAINHAND,
    'OFFHAND': OFFHAND,
    'FEET': FEET,
    'ACCESSORY': ACCESSORY
}

_key_to_slots = {
    'w': HEAD,
    's': TORSO,
    'q': MAINHAND,
    'a': OFFHAND,
    'd': FEET,
    'e': ACCESSORY
}
