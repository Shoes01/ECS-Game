class JobComponent:
    def __init__(self, job, upkeep):
        self.job = job
        self.upkeep = {
            'hp': 0,
            'attack': 0,
            'magic': 0,
            'speed': 0,
            'defense': 0,
            'resistance': 0
        }
        for stat, value in upkeep.items():
            self.upkeep[stat] = -10 * value # Negative because substracting dicts is hard; x10 because of the decimal display.