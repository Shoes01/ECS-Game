import attr

@attr.s(auto_attribs=True, slots=True)
class RaceComponent:
    ' Component identifying the race of the entity. '
    name: str

    def update(self, race):
        self.name = race.name