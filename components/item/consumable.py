class ConsumableComponent():
    def __init__(self, effects):
        self.effects = {} if effects is True else effects # type: a dict of effects