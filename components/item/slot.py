import attr

from _data import Slots

@attr.s(slots=True, auto_attribs=True)
class SlotComponent:
    ' Component that represents to which slot the item is equipped. '
    slot: Slots