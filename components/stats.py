import data.stats as Stats

class StatsComponent:
    ' Component that holds the stats of the entity. '
    ' Everything is multiplied by 10 in order to use pseudo decimals. ' # TODO: I should change this. Pseudo-decimals should only be used to _display_
    def __init__(self, stats_data):
        self.hp = stats_data[Stats.HP] * 10
        self.attack = stats_data[Stats.ATK] * 10
        self.defense = stats_data[Stats.DEF] * 10
        self.magic = stats_data[Stats.MAG] * 10
        self.resistance = stats_data[Stats.RES] * 10
        self.speed = stats_data[Stats.SPD] * 10
