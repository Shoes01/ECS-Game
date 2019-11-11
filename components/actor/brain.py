import attr

from _data import AI

@attr.s(slots=True)
class BrainComponent:
    ' Component that provides the AI to the entity. '
    brain: AI = attr.ib(default=AI.ZOMBIE)
    awake: bool = attr.ib(default=False)