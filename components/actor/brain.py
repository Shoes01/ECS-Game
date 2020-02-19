import attr

from _data import AI

@attr.s(auto_attribs=True, slots=True)
class BrainComponent:
    ' Component that provides the AI to the entity. '
    brain: AI = AI.ZOMBIE
    awake: bool = False