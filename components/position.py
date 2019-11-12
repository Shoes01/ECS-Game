import attr

@attr.s(slots=True, auto_attribs=True)
class PositionComponent:
    ' Component that holds the position of the entity. '
    x: int = 0
    y: int = 0