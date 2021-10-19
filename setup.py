from setuptools import setup, find_packages

try:
    with open("Readme_pypi.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Perlin Noise Generator"

setup(name='perlin_noise',
      version='1.8',
      description='Python implementation for Perlin Noise with unlimited coordinates space',
      author="salaxieb",
      author_email='salaxieb.ildar@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(include=['perlin_noise']),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
