from collections import namedtuple

import data.eccentricities as Eccentricities
import data.rarities as Rarities

Soul = namedtuple('soul', 'eccentricity rarity new_game', defaults=(False))

DEMON = Soul(
    eccentricity=Eccentricities.SUPERBOLIC,
    rarity=Rarities.MYTHIC
)

PLAYER = Soul(
    eccentricity=Eccentricities.CIRCULAR,
    rarity=Rarities.MYTHIC,
    new_game=True
)

ZOMBIE = Soul(
    eccentricity=Eccentricities.HYPOBOLIC,
    rarity=Rarities.AWFUL
)

all = {'DEMON': DEMON, 'PLAYER': PLAYER, 'ZOMBIE': ZOMBIE}
