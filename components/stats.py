import attr

@attr.s(auto_attribs=True)
class StatsComponent:
    ' Component that holds the stats of the entity. '
    hp: int = 0
    attack: int = 0
    defense: int = 0
    magic: int = 0
    resistance: int = 0
    speed: int = 0

    def __attrs_post_init__(self):
        ' Everything is multiplied by 10 in order to use pseudo decimals. '
        self.hp *= 10
        self.attack *= 10
        self.defense *= 10
        self.magic *= 10
        self.resistance *= 10
        self.speed *= 10