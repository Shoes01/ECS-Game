import numpy as np

class ItemSkillComponent():
    def __init__(self, cost, name, east, north_east):
        self.cost = cost
        self.name = name
        self.east = np.array(east)
        self.north = np.rot90(self.east)
        self.west = np.rot90(self.north)
        self.south = np.rot90(self.west)
        self.north_east = np.array(north_east)
        self.north_west = np.rot90(self.north_east)
        self.south_west = np.rot90(self.north_west)
        self.south_east = np.rot90(self.south_west)
        