class StatsComponent():
    def __init__(self, hp=None, power=None):
        self.hp = 1 if hp is None else hp
        self.hp_max = self.hp
        self.power = 0 if power is None else power