import attr

from _data import RACES

@attr.s(slots=True, auto_attribs=True)
class RaceComponent:
    ' Component identifying the race of the entity. '
    race: RACES = RACES.HUMAN