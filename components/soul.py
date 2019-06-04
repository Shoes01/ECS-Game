import numpy as np
import random

class SoulComponent:
    """
    The soul is a 2x3 matrix whose values are added to the stats of the unit.
    The stats are decided in this way:
    [[  HP, ATK, MAG],
     [ SPD, DEF, RES]]
    """
    def __init__(self, eccentricity, max_rarity):
        self.eccentricity = eccentricity
        self.max_rarity = max_rarity
        
        self.np_soul = self.generate_soul()

    @property
    def soul(self):
        soul = {}
        soul['hp'] = self.np_soul[0][0]
        soul['speed'] = self.np_soul[1][0]
        soul['attack'] = self.np_soul[0][1]
        soul['defense'] = self.np_soul[1][1]
        soul['magic'] = self.np_soul[0][2]
        soul['resistance'] = self.np_soul[1][2]

        return soul

    def generate_soul(self):
        attempts = 0
        eccentricity = self.eccentricity
        rarity = random.randint(-2, self.max_rarity) # -2 is the floor for max_rarity: it represents Zombie
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