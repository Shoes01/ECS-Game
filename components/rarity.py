import attr

from _data import Rarities

@attr.s(slots=True, auto_attribs=True)
class RarityComponent:
    ' Component that holds the rarity of the item. '
    rarity: Rarities