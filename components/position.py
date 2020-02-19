import attr

@attr.s(auto_attribs=True, slots=True)
class PositionComponent:
    ' Component that holds the position of the entity. '
    x: int = 0
    y: int = 0