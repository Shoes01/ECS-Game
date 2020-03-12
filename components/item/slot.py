import attr
import data.slots as Slots

@attr.s(auto_attribs=True, slots=True)
class SlotComponent:
    ' Component that represents to which slot the item is equipped. '
    name: str
    key: str