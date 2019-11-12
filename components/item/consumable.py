import attr

from typing import Dict

@attr.s(slots=True)
class ConsumableComponent:
    ' Component bestows an item with an effect when used. '
    effects: Dict[str, int] = attr.ib(factory=dict) # Example of effect: {'heal': 10}