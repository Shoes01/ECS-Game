import attr

@attr.s(auto_attribs=True, slots=True)
class TileComponent:
    ' Component that holds the pathing/fov information of a tile entity. '
    blocks_path: bool = True
    blocks_sight: bool = True