import math, random

class RandVec:
    def __init__(self, coordinates, seed=None):
        """
         Vector initialized in cpecified coordinates, helper for perlin noise
        """
        self.coordinates = coordinates
        self.vec = self.sample_vector(dimensions=len(self.coordinates), seed=seed)

    def dists_to(self, coordinates):
        dists = list(map(lambda x: x[0]-x[1], zip(coordinates, self.coordinates)))
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


class PerlinNoise:
    """
    Smooth random noise generator
    read more https://en.wikipedia.org/wiki/Perlin_noise
    """
    def __init__(self, n_dims=1, octaves=1, seed=None):
        """
            Perlin Noise object initialisation class
            ex.: noise = PerlinNoise(n_dims=2, octaves=3.5, seed=777)
            n_dims : positive int, optional, default = 1
                space dimension
            octaves : positive float, obtional, default = 1
                positive number of sub rectangles in each [0, 1] range
            seed : positive int, optional, default = None
                specific seed with which you want to initialize random generator
        """
        try:
            assert type(n_dims) == int and n_dims > 0
        except AssertionError:
            raise ValueError(f'n_dims expected to be positive integer number, but you passed: {n_dims}')

        try:
            assert octaves > 0
        except AssertionError:
            raise ValueError(f'octaves expected to be positive number, but you passed: {octaves}')

        try:
            if not seed is None:
                assert type(seed) == int and seed > 0
        except AssertionError:
            raise ValueError(f'seed expected to be positive integer number, but you passed: {seed}')

        self.n_dims = n_dims
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
        return max(1, abs(RandVec._dot([10^p for p in range(len(coors))], coors)+1))

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
            if self.n_dims == 1:
                return
            else:
                raise TypeError('if n_dims > 1 coordinates must be iterable of coordinates')
        else:
            if self._is_iterable(coordinates):
                if len(list(coordinates)) == self.n_dims:
                    return
                else:
                    raise TypeError(f'''
                                    coordinates must be iterable (np.array, list, map ..)
                                    with len(coordinates) = n_dims,
                                    but you passed coordinates with length {len(coordinates)}
                                    and n_dims = {self.n_dims}''')
            else:
                raise TypeError(f'''
                                coordinates must be iterable (np.array, list, map ..)
                                with len(coordinates) = n_dims,
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
        coordinates - integer if n_dims==1 or list of coordinates with length = n_dims
        """
        self._is_valid_coordinates(coordinates)

        if type(coordinates) == int or type(coordinates) == float:
            coordinates = [coordinates]

        coordinates = list(map(lambda x: x*self.octaves, coordinates))
        try:
            coor_bounding_box = [[math.floor(c), math.floor(c+1)] for c in coordinates]
        except TypeError:
            raise TypeError(f'''could execute math.floor to passed coordinated,
                                expected int or float, reveived {coordinates[0]}''')

        val = 0
        for coors in self._each_with_each(coor_bounding_box):
            h = self._hasher(coors)
            seed = self.seed * h
            val += RandVec(coors, seed).get_weighted_val(coordinates)
        return val

    def __call__(self, coordinates):
        """ forward request to noise function """
        return self.noise(coordinates)
