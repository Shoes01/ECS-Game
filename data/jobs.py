import data.races as Races

MONSTER = {
    'description': "Placeholder job for monsters.",
    'name': 'monster job',
    'races': (Races.MONSTER,),
    'skills': {},
    'upkeep': {}
}
SOLDIER = {
    'description': "Baby's first job.",
    'name': 'soldier', 
    'races': (Races.HUMAN,),
    'skills': {},
    'upkeep': {}
}
WARRIOR = {
    'description': 'Has access to more devastating skills.', # Not rly.
    'name': 'warrior',
    'races': (Races.HUMAN,),
    'skills': {},
    'upkeep': {'magic': 1, 'speed': 2}
}
BERSERKER = {
    'description': 'Classic orc.',
    'name': 'berserker',
    'races': (Races.ORC,),
    'skills': {},
    'upkeep': {'speed': 1, 'hp': 1}
}
ROGUE = {
    'description': 'A job for seasoned fighters.',
    'name': 'rogue',
    'races': (Races.HUMAN, Races.GOBLIN, Races.ELF),
    'skills': {'soldier': 1},
    'upkeep': {'speed': 1, 'hp': 15}
}
THIEF = {
    'description': 'A stealer.',
    'name': 'thief',
    'races': (Races.HUMAN,),
    'skills': {},
    'upkeep': {}
}

all = {
    'MONSTER': MONSTER, 
    'SOLDIER': SOLDIER, 
    'WARRIOR': WARRIOR, 
    'BERSERKER': BERSERKER, 
    'ROGUE': ROGUE, 
    'THIEF': THIEF
}
