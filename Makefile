test:
	@python -m pytest

lint:
	@mypy perlin_noise
	@flake8 perlin_noise --ignore WPS412 # Found `__init__.py` module with logic

tox:
	@tox