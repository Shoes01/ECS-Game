class ConsumableComponent():
    def __init__(self, effects):
        self.effects = {} if effects is None else effects # type: a dict of effects