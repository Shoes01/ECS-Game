import attr

from _data import Races

@attr.s(slots=True, auto_attribs=True)
class RaceComponent:
    ' Component identifying the race of the entity. '
    race: Races = Races.HUMAN