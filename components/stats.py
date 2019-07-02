class StatsComponent():
    def __init__(self, hp=None, attack=None, defense=None, magic=None, resistance=None, speed=None):
        # Everything is * 10'd in order to use pseudo decimals.
        self.hp = 0 if hp is None else hp * 10
        self.attack = 0 if attack is None else attack * 10
        self.defense = 0 if defense is None else defense * 10
        self.magic = 0 if magic is None else magic * 10
        self.resistance = 0 if resistance is None else resistance * 10
        self.speed = 0 if speed is None else speed * 10