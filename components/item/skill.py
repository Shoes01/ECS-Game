import numpy as np

class ItemSkillComponent():
    def __init__(self, cooldown, cost_energy, cost_soul, name, damage_type, description, east, north_east):
        ' Skill data. '
        self.cooldown = cooldown
        self.cooldown_remaining = 0
        self.cost_energy = cost_energy
        self.cost_soul = cost_soul
        self.description = description
        self.name = name
        self.damage_type = damage_type

        ' Skill directions. '
        self.east = np.array(east)
        self.north = np.rot90(self.east)
        self.west = np.rot90(self.north)
        self.south = np.rot90(self.west)
        self.north_east = np.array(north_east)
        self.north_west = np.rot90(self.north_east)
        self.south_west = np.rot90(self.north_west)
        self.south_east = np.rot90(self.south_west)
        