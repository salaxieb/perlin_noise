"""Perlin Noise calculating lib."""
import math
import random
from collections.abc import Iterable
from typing import Dict, Optional, Tuple, Union
import itertools

from perlin_noise.rand_vec import RandVec
from perlin_noise.tools import hasher


class PerlinNoise(object):
    """Smooth random noise generator.

    read more https://en.wikipedia.org/wiki/Perlin_noise
    """

    def __init__(self, octaves: float = 1, seed: Optional[int] = None):
        """Perlin Noise object initialization class.

            ex.: noise = PerlinNoise(n_dims=2, octaves=3.5, seed=777)

        Parameters:
            octaves : optional positive float, default = 1
                positive number of sub rectangles in each [0, 1] range
            seed : optional positive int, default = None
                specified seed

        Raises:
            ValueError: if seed is negative
        """
        if octaves <= 0:
            raise ValueError('octaves expected to be positive number')

        if seed is not None and not isinstance(seed, int) and seed <= 0:
            raise ValueError('seed expected to be positive integer number')

        self.octaves: float = octaves
        self.seed: int = seed if seed else random.randint(1, 10**5)  # noqa: S311, E501
        self.cache: Dict[Tuple, RandVec] = {}

    def __call__(self, coordinates: Union[int, float, Iterable]) -> float:
        """Forward request to noise function.

        Parameters:
            coordinates: float or list of coordinates

        Returns:
            noise_value
        """
        return self.noise(coordinates)

    def noise(self, coordinates: Union[int, float, Iterable]) -> float:
        """Get perlin noise value for given coordinates.

        Parameters:
            coordinates: float or list of coordinates

        Returns:
            noise_value

        Raises:
            TypeError: if coordinates is not valid type
        """
        if not isinstance(coordinates, (int, float, Iterable)):
            raise TypeError('coordinates must be int, float or iterable')

        if isinstance(coordinates, (int, float)):
            coordinates = [coordinates]

        coordinates = list(
            map(lambda coordinate: coordinate * self.octaves, coordinates),
        )

        coor_bounding_box = [
            (math.floor(coordinate), math.floor(coordinate) + 1)
            for coordinate in coordinates
        ]
        return sum([
            self.get_from_cache_of_create_new(coors).get_weighted_val(coordinates)
            for coors in itertools.product(*coor_bounding_box)
        ])

    def get_from_cache_of_create_new(self, coors):
        """Use cached RandVec or creates new.

        Parameters:
            coors: Tuple of int vector coordinates

        Returns:
            RandVec
        """
        if coors not in self.cache:
            self.cache[coors] = RandVec(
                coors, self.seed * hasher(coors),
            )
        return self.cache[coors]
