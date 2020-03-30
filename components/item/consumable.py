import attr

@attr.s(auto_attribs=True, frozen=True, slots=True)
class ConsumableComponent:
    ' Component bestows an item with an effect when used. '
    effects: dict = attr.Factory(dict) # Example of effect: {'heal': 10}