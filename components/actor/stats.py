class StatsComponent():
    def __init__(self, hp=None, attack=None, defense=None, magic=None, resistance=None, speed=None):
        self.hp = 1 if hp is None else hp
        self.hp_max = self.hp
        self.attack = 0 if attack is None else attack
        self.defense = 0 if defense is None else defense
        self.magic = 0 if magic is None else magic
        self.resistance = 0 if resistance is None else resistance
        self.speed = 0 if speed is None else speed