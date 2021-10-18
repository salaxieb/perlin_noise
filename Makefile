test:
	@python -m pytest

lint:
	@mypy perlin_noise
	@flake8 perlin_noise