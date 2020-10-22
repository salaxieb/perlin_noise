import math
import random

class RandVec:
    def __init__(self, coordinates, seed=None):
        """
         Vector initialized in cpecified coordinates, helper for perlin noise
        """
        self.coordinates = coordinates
        self.vec = self.sample_vector(dimensions=len(self.coordinates), seed=seed)

    def dists_to(self, coordinates):
        dists = [x[0]-x[1] for x in zip(coordinates, self.coordinates)]
        return dists

    def multiply_arr(self, arr):
        if len(arr)==1:
            return arr[0]
        else:
            return arr[0]*self.multiply_arr(arr[1:])

    def weight_to(self, coordinates):
        weighted_dists = list(map(lambda x: self.fade(1-abs(x)), self.dists_to(coordinates)))
        return self.multiply_arr(weighted_dists)

    def get_weighted_val(self, coordinates):
        return self.weight_to(coordinates)*self._dot(self.vec, self.dists_to(coordinates))

    @staticmethod
    def sample_vector(dimensions, seed=None):
        """ sampling normilized vector length 1"""
        if seed:
            st = random.getstate()
            random.seed(seed)

        vec = []
        for d in range(dimensions):
            vec.append(random.uniform(-1, 1))

        if seed:
            random.setstate(st)

        norm = math.sqrt(RandVec._dot(vec, vec))
        norm = math.sqrt(len(vec))
        vec = [math.sqrt(len(vec))*v/norm for v in vec]
        return vec

    @staticmethod
    def _dot(vec1, vec2):
        """ two vectors dot product """
        try:
            assert len(vec1) == len(vec2)
        except AssertionError:
            raise ValueError('lengths of two vectors are not equal')
        return sum([v * w for v, w in zip(vec1, vec2)])

    @staticmethod
    def fade(val):
        """ fade - [0, 1] values smothing function"""
        try:
            assert val >= 0 and val <= 1
        except AssertionError:
            raise ValueError(f'expected to have value in range [0, 1] but you passed {val}')
        return 6*math.pow(val, 5)-15*math.pow(val,4)+10*math.pow(val,3)
