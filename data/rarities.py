import attr

# Rarities
@attr.s(auto_attribs=True, slots=True)
class Rarity:
    eccentricity: int # The greater the eccentricity, the greater the variation in base stats.
    name: str         # The name of this type of eccentricity.
    rank: int         # The rank of the rarity. 0 is lowest.

AWFUL = Rarity(eccentricity=-2, name="decayed", rank=0)
POOR = Rarity(eccentricity=-1, name="hypobolic", rank=1)
COMMON = Rarity(eccentricity= 0, name="circular", rank=2)
UNCOMMON = Rarity(eccentricity= 1, name="elliptic", rank=3)
EPIC = Rarity(eccentricity= 3, name="parabolic", rank=4)
RARE = Rarity(eccentricity= 5, name="superbolic", rank=5)
MYTHIC = Rarity(eccentricity= 9, name="hyperbolic", rank=6)

all = {
    'AWFUL': AWFUL,
    'POOR': POOR,
    'COMMON': COMMON,
    'UNCOMMON': UNCOMMON,
    'EPIC': EPIC,
    'RARE': RARE,
    'MYTHIC': MYTHIC
}