import data.eccentricities as Eccentricities
import data.rarities as Rarities

SOUL = {
    'new_game': False
}

DEMON = {**SOUL,
    'eccentricity': Eccentricities.SUPERBOLIC,
    'rarity': Rarities.MYTHIC
}

PLAYER = {**SOUL,
    'eccentricity': Eccentricities.CIRCULAR,
    'new_game': True,
    'rarity': Rarities.MYTHIC
}

ZOMBIE = {**SOUL,
    'eccentricity': Eccentricities.HYPOBOLIC,
    'rarity': Rarities.AWFUL
}

all = {'DEMON': DEMON, 'PLAYER': PLAYER, 'ZOMBIE': ZOMBIE}
