import numpy as np

class SkillComponent:
    def __init__(self, ap_max, cooldown, cost_energy, cost_soul, damage_type, description, job_req, name, east, north_east):
        ' Skill flags. '
        self.is_active = False
        
        ' Skill data. '
        self.ap = 0
        self.ap_max = ap_max
        self.cooldown = cooldown
        self.cooldown_remaining = 0
        self.cost_energy = cost_energy # Type: int
        self.cost_soul = cost_soul # Type: dict{'stat': int}
        self.damage_type = damage_type
        self.description = description
        self.job_req = job_req # Type: str. Should only ever be one job req per skill.
        self.name = name

        ' Skill directions. '
        self.east = np.array(east)
        self.north = np.rot90(self.east)
        self.west = np.rot90(self.north)
        self.south = np.rot90(self.west)
        self.north_east = np.array(north_east)
        self.north_west = np.rot90(self.north_east)
        self.south_west = np.rot90(self.north_west)
        self.south_east = np.rot90(self.south_west)

    @property
    def is_mastered(self):
        if self.ap == self.ap_max:
            return True
        return False