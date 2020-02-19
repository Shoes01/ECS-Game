import attr

from _data import Races

@attr.s(auto_attribs=True, slots=True)
class RaceComponent:
    ' Component identifying the race of the entity. '
    race: Races = Races.HUMAN