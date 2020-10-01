Smooth random noise generator  
read more https://en.wikipedia.org/wiki/Perlin_noise  


noise = PerlinNoise(n_dims=2, octaves=3.5, seed=777)  
  <span>n_dims : positive int, optional, default = 1  
       <span><span>space dimension  
   <span>octaves : positive float, obtional, default = 1  
       <span><span>positive number of sub rectangles in each [0, 1] range  
   <span><span>seed : positive int, optional, default = None  
       <span><span>specific seed with which you want to initialize random generator  

Usage examples:
```python
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(n_dims=2, octaves=2)
xpix = 100
ypix = 100
pic = []
for i in range(xpix):
    row = []
    for j in range(ypix):
        row.append(noise([i/xpix, j/ypix]))
    pic.append(row)

plt.imshow(arr, cmap='gray')
plt.show()
```
![png](pics/output_4_0.png)

```python
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise1 = PerlinNoise(n_dims=2, octaves=1)
noise2 = PerlinNoise(n_dims=2, octaves=2)
noise3 = PerlinNoise(n_dims=2, octaves=4)
noise4 = PerlinNoise(n_dims=2, octaves=8)

xpix = 100
ypix = 100
pic = []
for i in range(xpix):
    row = []
    for j in range(ypix):
        noise_val =         noise1([i/xpix, j/ypix])
        noise_val += 0.5  * noise2([i/xpix, j/ypix])
        noise_val += 0.25 * noise3([i/xpix, j/ypix])
        noise_val += 0.125* noise4([i/xpix, j/ypix])

        row.append(noise_val)
    pic.append(row)

plt.imshow(pic, cmap='gray')
plt.show()
```

![png](pics/output_5_0.png)
