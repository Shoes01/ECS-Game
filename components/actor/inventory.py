import attr

from typing import List

@attr.s(slots=True)
class InventoryComponent:
    ' Component holds a list of entity IDs representing held items. '
    inventory: List[int] = attr.ib(factory=list)