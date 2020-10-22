import math, random
from .RandVec import RandVec

class PerlinNoise:
    """
    Smooth random noise generator
    read more https://en.wikipedia.org/wiki/Perlin_noise
    """
    def __init__(self, octaves=1, seed=None):
        """
            Perlin Noise object initialisation class
            ex.: noise = PerlinNoise(n_dims=2, octaves=3.5, seed=777)
            octaves : positive float, obtional, default = 1
                positive number of sub rectangles in each [0, 1] range
            seed : positive int, optional, default = None
                specific seed with which you want to initialize random generator
        """

        try:
            assert octaves > 0
        except AssertionError:
            raise ValueError(f'octaves expected to be positive number, but you passed: {octaves}')

        try:
            if not seed is None:
                assert type(seed) == int and seed > 0
        except AssertionError:
            raise ValueError(f'seed expected to be positive integer number, but you passed: {seed}')

        self.octaves = octaves
        if seed:
            self.seed = seed
        else:
            self.seed = random.randint(1, 10^5)

    def _hasher(self, coors):
        """
        hashes coordinates to integer number to avoid repeats in seed
        coors - array of coordinates
        """
        return max(1, abs(RandVec._dot([10**p for p in range(len(coors))], coors)+1))

    @staticmethod
    def _is_iterable(obj):
        """ checks is given object iterable """
        try:
            iter(obj)
        except Exception:
            return False
        else:
            return True

    def _is_valid_coordinates(self, coordinates):
        """
        internal function that checks if given coordinates are valid
        """
        if type(coordinates) == int or type(coordinates) == float:
            return
        else:
            if not self._is_iterable(coordinates):
                raise TypeError(f'''
                                coordinates must be iterable (np.array, list, map ..)
                                but you passed not iterable coordinates of type {type(coordinates)}''')

    @staticmethod
    def _each_with_each(arrs, prev=(), results=[]):
        """
            creates iterable for given array of arrays
            where each value connected
            with each value from each array
        """
        for el in arrs[0]:
            new = prev + (el,)
            if len(arrs) == 1:
                yield new
            else:
                yield from PerlinNoise._each_with_each(arrs[1:], prev=new, results=results)

    def noise(self, coordinates):
        """
        basic function that returns noise value for given coordinates
        coordinates - integer or list of coordinates
        """
        self._is_valid_coordinates(coordinates)

        if type(coordinates) == int or type(coordinates) == float:
            coordinates = [coordinates]

        coordinates = list(map(lambda x: x*self.octaves, coordinates))
        try:
            coor_bounding_box = [(math.floor(c), math.floor(c+1)) for c in coordinates]
        except TypeError:
            raise TypeError(f'''could execute math.floor to passed coordinated,
                                expected int or float, reveived {type(coordinates[0])}''')

        val = 0
        for coors in self._each_with_each(coor_bounding_box):
            h = self._hasher(coors)
            seed = self.seed * h
            val += RandVec(coors, seed).get_weighted_val(coordinates)
        return val

    def __call__(self, coordinates):
        """ forward request to noise function """
        return self.noise(coordinates)
