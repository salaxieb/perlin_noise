"""Perlin Noise calculating lib."""
import math
import random
from collections.abc import Iterable
from typing import Dict, Optional, Tuple, Union, List
import itertools
from functools import lru_cache

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

    def __call__(self, coordinates: Union[int, float, Iterable], tile_sizes: Optional[Union[int, List, Tuple]] = None) -> float:
        """Forward request to noise function.

        Parameters:
            coordinates: float or list of coordinates
            tile_sizes: optional tile sizes to repetative patterns

        Returns:
            noise_value
        """
        return self.noise(coordinates, tile_sizes)

    def noise(self, coordinates: Union[int, float, Iterable], tile_sizes: Optional[Union[int, List, Tuple]] = None) -> float:
        """Get perlin noise value for given coordinates.

        Parameters:
            coordinates: float or list of coordinates
            tile_sizes: optional tile sizes to repetative patterns

        Returns:
            noise_value

        Raises:
            TypeError: if coordinates is not valid type
        """
        if not isinstance(coordinates, (int, float, Iterable)):
            raise TypeError('coordinates must be int, float or iterable')

        if tile_sizes is not None:
            if not (isinstance(tile_sizes, int) or (isinstance(tile_sizes, (tuple, list)) and all(isinstance(tile, int) for tile in tile_sizes))):
                raise TypeError('tile_sizes must be int or list of int')

        
        if isinstance(coordinates, (int, float)):
            coordinates = [coordinates]
        else:
            coordinates = list(coordinates)

    
        if tile_sizes is not None:
            if isinstance(tile_sizes, int):
                tile_sizes = [tile_sizes]
            if len(tile_sizes) != len(coordinates):
                raise ValueError('tile_sizes must have same length as coordinates')
            
            coordinates = [coordinate % tile for coordinate, tile in zip(coordinates, tile_sizes)]
            tile_sizes = tuple(tile * self.octaves for tile in tile_sizes)
        coordinates = [coordinate * self.octaves for coordinate in coordinates]
    

        coor_bounding_box = [
            (math.floor(coordinate), math.floor(coordinate) + 1)
            for coordinate in coordinates
        ]
        return sum([
            self.get_from_cache_of_create_new(coors, tile_sizes).get_weighted_val(coordinates)
            for coors in itertools.product(*coor_bounding_box)
        ])

    @lru_cache(maxsize=100, typed=False)
    def get_from_cache_of_create_new(self, coors: Tuple[int, ...], tile_sizes: Optional[Tuple[int, ...]] = None) -> RandVec:
        """Use cached RandVec or creates new.

        Parameters:
            coors: Tuple of int vector coordinates

        Returns:
            RandVec
        """
        return RandVec(coors, self.seed * hasher(coors, tile_sizes))
