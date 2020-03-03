import attr
import data.ai as AI

@attr.s(auto_attribs=True, slots=True)
class BrainComponent:
    ' Component that provides the AI to the entity. '
    brain: AI = AI.ZOMBIE
    awake: bool = False