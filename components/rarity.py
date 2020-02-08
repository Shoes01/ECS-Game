import attr

from _data import RARITIES

@attr.s(slots=True, auto_attribs=True)
class RarityComponent:
    ' Component that holds the rarity of the item. '
    rarity: RARITIES