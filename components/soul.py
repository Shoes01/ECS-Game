import data.stats as Stats
import numpy as np
import random

class SoulComponent:
    """An entity's soul.

    The soul is a 2x3 matrix whose values are added to the stats of the unit.
    The stats are decided in this way:
    [[  HP, ATK, MAG],
     [ SPD, DEF, RES]]
    """
    def __init__(self, eccentricity, rarity, new_game):
        self.eccentricity = eccentricity # Provides variation to the soul.
        self.max_rarity = rarity # "Rarer" entities have bigger values in their soul. 
        
        if new_game:
            self.np_soul = np.zeros((2, 3), dtype=int, order='F')
        else:
            self.np_soul = self.generate_soul()

    @property
    def soul(self):
        return {
            Stats.HP:  self.np_soul[0][0],
            Stats.ATK: self.np_soul[1][0],
            Stats.DEF: self.np_soul[0][1],
            Stats.MAG: self.np_soul[1][1],
            Stats.RES: self.np_soul[0][2],
            Stats.SPD: self.np_soul[1][2]
        }

    def generate_soul(self):
        attempts = 0
        eccentricity = self.eccentricity.rank
        rarity = random.randint(-2, self.max_rarity.rank) # -2 is the floor for max_rarity: it represents Zombie
        soul_attempt = np.zeros((2, 3), dtype=int, order='F')

        if eccentricity * 6 < rarity:
            print('WARNING: This could is impossible to make.')
            eccentricity += 2

        while attempts < 400:
            with np.nditer(soul_attempt, op_flags=['readwrite']) as it:
                for x in it:
                    x[...] = random.randint(-eccentricity, eccentricity)
            
            if soul_attempt.sum() == rarity:
                return soul_attempt

            attempts += 1
            if attempts > 300:
                rarity = 3 * rarity // 4
        
        print('Soul failed. Rank: {0}. Eccentricity: {1}'.format(rarity, eccentricity))
        return np.zeros((2, 3), dtype=int, order='F')