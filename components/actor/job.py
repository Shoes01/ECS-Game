class JobComponent:
    def __init__(self, job, upkeep):
        # TODO: Streamline this with  the new _job.py file.
        self.job = job
        self.upkeep = {
            'hp': 0,
            'attack': 0,
            'magic': 0,
            'speed': 0,
            'defense': 0,
            'resistance': 0
        }
        
        self.update_upkeep(upkeep)
    
    def update_upkeep(self, upkeep):
        new_upkeep = {
            'hp': 0,
            'attack': 0,
            'magic': 0,
            'speed': 0,
            'defense': 0,
            'resistance': 0
        }
        
        for stat, value in upkeep.items():
            new_upkeep[stat] = -10 * value # Negative because substracting dicts is hard; x10 because of the decimal display.
        
        self.upkeep = new_upkeep