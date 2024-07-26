"""Random vector generator used for weighting perlin noise."""

from functools import reduce
from operator import mul
from typing import List, Tuple

from perlin_noise.tools import dot, fade, sample_vector


class RandVec:
    """Vectors to give weights and contribute in final value."""

    def __init__(self, coordinates: Tuple[int, ...], seed: int):
        """Vector initializer in specified coordinates.

        Parameters:
            coordinates: Tuple[int] - vector coordinates
            seed: int - random init seed
        """
        self.coordinates = coordinates
        self.vec = sample_vector(dimensions=len(self.coordinates), seed=seed)

    def dists_to(self, coordinates: List[float]) -> Tuple[float, ...]:
        """Calculate distance to given coordinates.

        Parameters:
            coordinates: Tuplie[int] - coordinates to calculate distance

        Returns:
            distance

        """
        return tuple(
            coor1 - coor2 for coor1, coor2 in zip(coordinates, self.coordinates)
        )

    def weight_to(self, coordinates: List[float]) -> float:
        """Calculate this vector weights to given coordinates.

        Parameters:
            coordinates: Tuple[int] - target coordinates

        Returns:
            weight
        """
        # fmt: off
        weighted_dists = [fade(1 - abs(dist)) for dist in self.dists_to(coordinates)]  # noqa: E501, WPS221
        # fmt: on
        return reduce(mul, weighted_dists)

    def get_weighted_val(self, coordinates: List[float]) -> float:
        """Calculate weighted contribution of this vec to final result.

        Parameters:
            coordinates: calculate weighted relative to this coordinates

        Returns:
            weighted contribution
        """
        return self.weight_to(coordinates) * dot(
            self.vec,
            self.dists_to(coordinates),
        )
