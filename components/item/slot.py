import attr

from _data import SLOTS

@attr.s(slots=True, auto_attribs=True)
class SlotComponent:
    ' Component that represents to which slot the item is equipped. '
    slot: SLOTS