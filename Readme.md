Smooth random noise generator  
read more https://en.wikipedia.org/wiki/Perlin_noise  


noise = PerlinNoise(octaves=3.5, seed=777)  
 &nbsp;&nbsp;&nbsp;&nbsp;octaves : number of sub rectangles in each [0, 1] range  
 &nbsp;&nbsp;&nbsp;&nbsp;seed : specific seed with which you want to initialize random generator  


```python
from perlin_noise import PerlinNoise


noise = PerlinNoise()
# accepts as argument float and/or list[float]
noise(0.5) == noise([0.5])
# --> True
# noise not limited in space dimension and seamless in any space size
noise([0.5, 0.5]) == noise([0.5, 0.5, 0, 0, 0])
# --> True
```

Usage examples:
```python
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=10, seed=1)
xpix, ypix = 100, 100
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

plt.imshow(pic, cmap='gray')
plt.show()
```
![png](pics/output_4_0.png)

```python
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

xpix, ypix = 100, 100
pic = []
for i in range(xpix):
    row = []
    for j in range(ypix):
        noise_val = noise1([i/xpix, j/ypix])
        noise_val += 0.5 * noise2([i/xpix, j/ypix])
        noise_val += 0.25 * noise3([i/xpix, j/ypix])
        noise_val += 0.125 * noise4([i/xpix, j/ypix])

        row.append(noise_val)
    pic.append(row)

plt.imshow(pic, cmap='gray')
plt.show()
```

![png](pics/output_5_0.png)


Library has a possibility to generate repetative random noise with custom tile sizes:

```python
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=2, seed=42)
xpix, ypix = 800, 1200
lim_x, lim_y = 6, 9
pic = [
    [
        noise([lim_x * i / xpix, lim_y * j / ypix], tile_sizes=[2, 3])
        for j in range(xpix)
    ]
    for i in range(ypix)
]

plt.imshow(pic, cmap="gray")
plt.show()
```

![png](pics/smooth_tiled.png)

```python
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise1 = PerlinNoise(octaves=1)
noise2 = PerlinNoise(octaves=3)
noise3 = PerlinNoise(octaves=6)
noise4 = PerlinNoise(octaves=12)

xpix, ypix = 800, 1200
lim_x, lim_y = 4, 6
tile_sizes = (2, 3)
pic = []
for i in range(ypix):
    row = []
    for j in range(xpix):
        noise_val = noise1([lim_x * i / xpix, lim_y * j / ypix], tile_sizes)
        noise_val += 0.5 * noise2([lim_x * i / xpix, lim_y * j / ypix], tile_sizes)
        noise_val += 0.25 * noise3([lim_x * i / xpix, lim_y * j / ypix], tile_sizes)
        noise_val += 0.125 * noise4([lim_x * i / xpix, lim_y * j / ypix], tile_sizes)

        row.append(noise_val)
    pic.append(row)

plt.imshow(pic, cmap="gray")
plt.savefig("pics/multy_noise_tiled.png", transparent=True)
plt.show()
```
![png](pics/multy_noise_tiled.png)

for tiles to work correctly, number of octaves **MUST** be integer
```python
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=2.5, seed=42)
xpix, ypix = 800, 1200
lim_x, lim_y = 6, 9
pic = [
    [
        noise([lim_x * i / xpix, lim_y * j / ypix], tile_sizes=(2, 3))
        for j in range(xpix)
    ]
    for i in range(ypix)
]

plt.imshow(pic, cmap="gray")
plt.savefig('pics/tiled_with_step.png', transparent=True)
plt.show()
```
![png](pics/tiled_with_step.png)