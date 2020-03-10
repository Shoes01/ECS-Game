import attr
import data.eccentricities as Eccentricities
import data.rarities as Rarities

class Soul:
    def __init__(self, eccentricity=Eccentricities.CIRCULAR, new_game=False, rarity=Rarities.COMMON):
        self.eccentricity = eccentricity
        self.new_game = new_game
        self.rarity = rarity        

PLAYER = Soul(
    eccentricity=Eccentricities.CIRCULAR,
    new_game=True,
    rarity=Rarities.MYTHIC
)

ZOMBIE = Soul(
    eccentricity=Eccentricities.HYPOBOLIC,
    rarity=Rarities.AWFUL
)

all = {'PLAYER': PLAYER, 'ZOMBIE': ZOMBIE}