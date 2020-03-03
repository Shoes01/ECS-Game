HEAD = 'head'
TORSO = 'torso'
MAINHAND = 'mainhand'
OFFHAND = 'offhand'
FEET = 'feet'
ACCESSORY = 'accessory'

all = {
    'HEAD': HEAD,
    'TORSO': TORSO,
    'MAINHAND': MAINHAND,
    'OFFHAND': OFFHAND,
    'FEET': FEET,
    'ACCESSORY': ACCESSORY
}

_slots_to_key = {
    HEAD: 'w',
    TORSO: 's',
    MAINHAND: 'q',
    OFFHAND: 'a',
    FEET: 'd',
    ACCESSORY: 'e'
}

_key_to_slots = {
    'w': HEAD,
    's': TORSO,
    'q': MAINHAND,
    'a': OFFHAND,
    'd': FEET,
    'e': ACCESSORY
}
