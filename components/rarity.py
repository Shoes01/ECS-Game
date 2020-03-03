import attr
import data.rarities as Rarities

@attr.s(auto_attribs=True, slots=True)
class RarityComponent:
    ' Component that holds the rarity of the item. '
    rarity: Rarities