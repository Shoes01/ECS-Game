import attr

from _data import AI

@attr.s(slots=True, auto_attribs=True)
class BrainComponent:
    ' Component that provides the AI to the entity. '
    brain: AI = AI.ZOMBIE
    awake: bool = False