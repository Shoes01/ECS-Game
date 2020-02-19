import attr

from _data import Slots

@attr.s(auto_attribs=True, slots=True)
class SlotComponent:
    ' Component that represents to which slot the item is equipped. '
    slot: Slots