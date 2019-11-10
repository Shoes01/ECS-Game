import attr

@attr.s(slots=True)
class RaceComponent:
    ' Component identifying the race of the entity. '
    race: str = attr.ib()# TODO: Eventually change from using strings to using actual AI classes, like I did with States.