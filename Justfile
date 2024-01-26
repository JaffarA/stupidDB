black:
    poetry run black .

isort:
    poetry run isort .

ruff:
    poetry run ruff check .

mypy:
    poetry run mypy .

format: black isort

lint: ruff mypy

test:
    poetry run coverage run -m pytest

coverage:
    poetry run coverage report -m
