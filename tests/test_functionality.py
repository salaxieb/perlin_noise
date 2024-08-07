import random

from perlin_noise import PerlinNoise


def test_perlin_noise_works_in_1D():
    """Check if values in -1 1 range and changes slowly"""
    p_noise = PerlinNoise()
    lim = 2000
    prev = 0
    for i in range(lim):
        noise = p_noise([i / lim])
        assert -1 < noise < 1
        assert 0 <= abs(noise - prev) < 0.001
        prev = noise


def test_perlin_noise_works_in_2D():
    """Check value in [-1, 1] range."""
    noise = PerlinNoise(octaves=13)
    lim = 100
    for i in range(lim):
        for j in range(lim):
            assert -1 <= noise([i / lim, j / lim]) <= 1


def test_perlin_noise_works_in_high_dimensions():
    """Checks if values in -1 1 in high dimensions."""
    n_dims = 10
    noise = PerlinNoise(octaves=3)
    vec = []
    n_passes = 100
    for check in range(n_passes):
        vec = []
        for dim in range(n_dims):
            vec.append(random.uniform(-10, 10))
        assert -1 <= noise(vec) <= 1


def test_noise_value_doesnt_depend_on_space_size():
    """Test that noise value independent from test size."""
    noise = PerlinNoise(octaves=4.6, seed=777)
    assert noise([0.5, 0.5]) == noise([0.5, 0.5, 0, 0])
    assert noise([0.5, 0]) == noise([0.5, 0, 0, 0, 0])
    assert noise(0.5) == noise([0.5, 0])


def test_that_dist_in_0_1_range():
    noise = PerlinNoise(octaves=20.496, seed=1337)
    assert noise([125 / 1281, 1152 / 1281])


def test_tiles_works():
    noise = PerlinNoise(octaves=1.496)
    assert noise(0.5, tile_sizes=1) == noise(0.5)
    assert noise([0.5, 0.5], tile_sizes=[43, 2345]) == noise([0.5, 0.5])
    assert noise([1.5, 1.5], tile_sizes=[1, 1]) == noise([0.5, 0.5])
    assert noise([2.5, 3.5], tile_sizes=[2, 3]) == noise([0.5, 0.5])


def test_tiles_seamless():
    p_noise = PerlinNoise(octaves=2)
    lim = 400
    prev = 0
    x_lim, y_lim = 5, 10
    for i in range(0, lim, 100):
        prev = p_noise([x_lim * i / lim, 0], tile_sizes=[2, 3])
        for j in range(lim):
            noise = p_noise([x_lim * i / lim, y_lim * j / lim], tile_sizes=[2, 3])
            assert -1 < noise < 1
            assert 0 <= abs(noise - prev) < 0.1
            prev = noise
