import attr

from _data import RACES

@attr.s(slots=True)
class RaceComponent:
    ' Component identifying the race of the entity. '
    race: RACES = attr.ib(default=RACES.HUMAN)