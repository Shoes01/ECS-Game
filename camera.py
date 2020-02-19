import attr

@attr.s(auto_attribs=True, slots=True)
class Camera:
    ' The camera represents the area that is rendered to the screen. '
    w: int
    h: int
    x: int = 0 # Top left coordinate.
    y: int = 0
    leash: int = 10 # Leash is calculated as a radius from the center. Manhattan distance.