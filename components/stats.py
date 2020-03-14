import data.stats as Stats

class StatsComponent:
    ' Component that holds the stats of the entity. '
    def __init__(self, stats):
        self.hp =           0 if  stats.get(Stats.HP)  is None else  stats.get(Stats.HP)
        self.attack =       0 if  stats.get(Stats.ATK) is None else  stats.get(Stats.ATK)
        self.defense =      0 if  stats.get(Stats.DEF) is None else  stats.get(Stats.DEF)
        self.magic =        0 if  stats.get(Stats.MAG) is None else  stats.get(Stats.MAG)
        self.resistance =   0 if  stats.get(Stats.RES) is None else  stats.get(Stats.RES)
        self.speed =        0 if  stats.get(Stats.SPD) is None else  stats.get(Stats.SPD)

    @property
    def as_dict (self):
        stats =  {
            Stats.HP: self.hp,
            Stats.ATK: self.attack,
            Stats.DEF: self.defense,
            Stats.MAG: self.magic,
            Stats.RES: self.resistance,
            Stats.SPD: self.speed
        }
        return stats