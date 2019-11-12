import attr

from _data import SLOTS

@attr.s(slots=True)
class SlotComponent():
    ' Component that represents to which slot the item is equipped. '
    slot: SLOTS