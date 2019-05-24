class StatsComponent():
    def __init__(self, hp=None, atk=None, dfn=None, mag=None, res=None, spd=None):
        self.hp = 1 if hp is None else hp
        self.hp_max = self.hp
        self.atk = 0 if atk is None else atk
        self.dfn = 0 if dfn is None else dfn
        self.mag = 0 if mag is None else mag
        self.res = 0 if res is None else res
        self.spd = 0 if spd is None else spd