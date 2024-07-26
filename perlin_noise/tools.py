"""File for placing functions used in library."""

import math
import random
from typing import List, Optional, Tuple, Union


def dot(
    vec1: Union[List, Tuple],
    vec2: Union[List, Tuple],
) -> Union[float, int]:
    """Two vectors dot product.

    Parameters:
        vec1: List[float] - first vector
        vec2: List[float] - second vector

    Returns:
        Dot product of 2 vectors

    Raises:
        ValueError: if length not equal
    """
    if len(vec1) != len(vec2):
        raise ValueError("lengths of two vectors are not equal")
    return sum([val1 * val2 for val1, val2 in zip(vec1, vec2)])


def sample_vector(dimensions: int, seed: int) -> List[float]:
    """Sample normalized vector given length.

    Parameters:
        dimensions: int - space size
        seed: Optional[int] - random seed value

    Returns:
        List[float] - normalized random vector of given size
    """
    st = random.getstate()
    random.seed(seed)

    vec = []
    for _ in range(dimensions):
        vec.append(random.uniform(-1, 1))  # noqa: S311

    random.setstate(st)
    return vec


def fade(given_value: float) -> float:
    """Smoothing [0, 1] values.

    Parameters:
        given_value: float [0, 1] value for smoothing

    Returns:
        smoothed [0, 1] value

    Raises:
        ValueError: if input not in [-0.1, 1.1]
    """
    if given_value < -0.1 or given_value > 1.1:  # noqa: WPS459, WPS432
        raise ValueError("expected to have value in [-0.1, 1.1]")
    return (
        6 * math.pow(given_value, 5)  # noqa: WPS432
        - 15 * math.pow(given_value, 4)  # noqa: WPS432, W503
        + 10 * math.pow(given_value, 3)  # noqa: WPS432, W503
    )


def hasher(
    coordinates: Tuple[int, ...],
    tile_sizes: Optional[Tuple[int, ...]] = None,
) -> int:
    """Hashes coordinates to integer number and use obtained number as seed.

    Parameters:
        coordinates: Tuple[int, ...] - tuple of coordinates
        tile_sizes: Optional[Tuple[int, ...]] - optional tile sizes

    Returns:
        hash of coordinates in integer
    """
    if tile_sizes:
        coordinates = tuple(
            coors % tile for coors, tile in zip(coordinates, tile_sizes)
        )
    # fmt: off
    return max(
        1,
        int(
            abs(
                dot([10**coordinate for coordinate in range(len(coordinates))], coordinates) + 1,  # noqa: E501, WPS221
            ),
        ),
    )
    # fmt: on


def product(iterable: Union[List, Tuple]) -> float:
    """Multiplies values of iterable  each with each.

    Parameters:
        iterable: - any iterable

    Returns:
        product of values
    """
    if len(iterable) == 1:
        return iterable[0]
    return iterable[0] * product(iterable[1:])
