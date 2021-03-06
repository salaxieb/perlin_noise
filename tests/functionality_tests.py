from perlin_noise import PerlinNoise
import random


def test_if_perlin_noise_works_in_1D():
    ''' checks if values in -1 1 range and changes slowly '''
    p_noise = PerlinNoise()
    lim = 2000
    prev = 0
    for i in range(lim):
        noise = p_noise([i/lim])
        assert -1 < noise < 1
        assert 0 <= abs(noise - prev) < 0.001
        prev = noise

def test_if_perlin_noise_works_in_2D():
    noise = PerlinNoise()
    lim = 100
    for i in range(lim):
        for j in range(lim):
            assert -1 < noise([i/lim, j/lim]) < 1


def test_if_perlin_noise_works_in_high_dimensions():
    ''' checks if values in -1 1 in high dimensions '''
    n_dims = 10
    noise = PerlinNoise(octaves=3)
    vec = []
    n_passes = 100
    for check in range(n_passes):
        vec = []
        for dim in range(n_dims):
            vec.append(random.uniform(-10, 10))
        assert -1 < noise(vec) < 1


def test_if_noise_value_doesnt_depend_on_space_size():
    ''' test that noise value independent from test size '''

    noise1 = PerlinNoise(octaves=4.6, seed=777)
    noise2 = PerlinNoise(octaves=4.6, seed=777)
    assert noise1([0.5, 0.5])==noise2([0.5, 0.5, 0, 0, 0])
    assert noise1([0.5, 0])==noise2([0.5, 0, 0, 0, 0])
    assert noise1(0.5) == noise1([0.5, 0])
