import attr

@attr.s(slots=True, auto_attribs=True)
class ConsumableComponent:
    ' Component bestows an item with an effect when used. '
    effects: dict = attr.Factory(dict) # Example of effect: {'heal': 10}