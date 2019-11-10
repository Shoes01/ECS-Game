import attr

@attr.s(slots=True)
class BrainComponent:
    ' Component that provides the AI to the entity. '
    brain: str = attr.ib(default='zombie') # TODO: Eventually change from using strings to using actual AI classes, like I did with States.
    awake: bool = attr.ib(default=False)