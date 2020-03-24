from collections import namedtuple

import data.components_master as Components
import data.eccentricities as Eccentricities

Soul = namedtuple('Soul', 'eccentricity rarity new_game', defaults=(False,))

DEMON = Soul(
    eccentricity=Eccentricities.SUPERBOLIC,
    rarity=Components.RARITIES.MYTHIC
)

PLAYER = Soul(
    eccentricity=Eccentricities.CIRCULAR,
    rarity=Components.RARITIES.MYTHIC,
    new_game=True
)

ZOMBIE = Soul(
    eccentricity=Eccentricities.HYPOBOLIC,
    rarity=Components.RARITIES.AWFUL
)

all = {'DEMON': DEMON, 'PLAYER': PLAYER, 'ZOMBIE': ZOMBIE}
