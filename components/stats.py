import data.stats as Stats

class StatsComponent:
    ' Component that holds the stats of the entity. '
    ' Everything is multiplied by 10 in order to use pseudo decimals. ' # TODO: I should change this. Pseudo-decimals should only be used to _display_
    def __init__(self, stats_data):
        self.hp =           0 if stats_data.get(Stats.HP)  is None else stats_data.get(Stats.HP)  * 10
        self.attack =       0 if stats_data.get(Stats.ATK) is None else stats_data.get(Stats.ATK) * 10
        self.defense =      0 if stats_data.get(Stats.DEF) is None else stats_data.get(Stats.DEF) * 10
        self.magic =        0 if stats_data.get(Stats.MAG) is None else stats_data.get(Stats.MAG) * 10
        self.resistance =   0 if stats_data.get(Stats.RES) is None else stats_data.get(Stats.RES) * 10
        self.speed =        0 if stats_data.get(Stats.SPD) is None else stats_data.get(Stats.SPD) * 10
