import attr

@attr.s(auto_attribs=True, slots=True)
class Rarity:
    ' The rarity of an entity determines its base power. More rare, more power. '
    name: str
    rank: int

AWFUL =     Rarity(name="awful",    rank=0)
POOR =      Rarity(name="poor",     rank=1)
COMMON =    Rarity(name="common",   rank=2)
UNCOMMON =  Rarity(name="uncommon", rank=3)
EPIC =      Rarity(name="epic",     rank=4)
RARE =      Rarity(name="rare",     rank=5)
MYTHIC =    Rarity(name="mythic",   rank=6)

all = {
    'AWFUL': AWFUL,
    'POOR': POOR,
    'COMMON': COMMON,
    'UNCOMMON': UNCOMMON,
    'EPIC': EPIC,
    'RARE': RARE,
    'MYTHIC': MYTHIC
}
