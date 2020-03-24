import attr

@attr.s(auto_attribs=True, slots=True)
class RarityComponent:
    ' Component that holds the rarity of the item. '
    name: str
    rank: int