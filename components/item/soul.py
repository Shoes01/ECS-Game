import numpy as np
import random

class SoulComponent:
    def __init__(self, eccentricity, max_rarity):
        self.eccentricity = eccentricity
        self.max_rarity = max_rarity
        
        self.soul = self.generate_soul()

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