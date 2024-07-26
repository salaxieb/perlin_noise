test:
	@python -m pytest

lint:
	@poetry run black perlin_noise --check
	@poetry run mypy perlin_noise
	@poetry run flake8p perlin_noise --toml-config ./pyproject.toml

tox:
	@tox