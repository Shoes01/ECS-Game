import attr

from typing import List

@attr.s(slots=True, auto_attribs=True)
class InventoryComponent:
    ' Component holds a list of entity IDs representing held items. '
    inventory: List[int] = attr.Factory(list)