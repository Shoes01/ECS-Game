import attr

@attr.s(slots=True, auto_attribs=True)
class InventoryComponent:
    ' Component holds a list of entity IDs representing held items. '
    inventory: list = attr.Factory(list)