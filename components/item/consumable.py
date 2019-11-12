import attr

@attr.s(slots=True)
class ConsumableComponent:
    ' Component bestows an item with an effect when used. '
    effects: dict = attr.ib(factory=dict) # Example of effect: {'heal': 10}