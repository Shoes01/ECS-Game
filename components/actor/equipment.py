import attr

from typing import List

@attr.s(slots=True)
class EquipmentComponent:
    ' Component holds a list of entity IDs representing equipped items. '
    equipment: List[int] = attr.ib(factory=list)