import attr

from _data import UI_COLORS

@attr.s(auto_attribs=True, slots=True)
class Cursor:
    ' Contains information relevant to the cursor that the user may summon. '
    active: bool = False
    char: str = 'X'
    color_fg: tuple = UI_COLORS['cursor']
    x: int = 0
    y: int = 0