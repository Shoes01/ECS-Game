import attr

@attr.s(auto_attribs=True, frozen=True, slots=True)
class RaceComponent:
    ' Component identifying the race of the entity. '
    name: str