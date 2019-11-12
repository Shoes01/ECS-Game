import attr

@attr.s(slots=True, auto_attribs=True)
class TileComponent:
    ' Component that holds the pathing/fov information of a tile entity. '
    blocks_path: bool = True
    blocks_sight: bool = True