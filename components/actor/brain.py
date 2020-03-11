import attr

@attr.s(auto_attribs=True, slots=True)
class BrainComponent:
    ' Component that provides the AI to the entity. '
    name: str
    awake: bool = False
