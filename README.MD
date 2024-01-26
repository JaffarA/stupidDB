>This project is designed for recreational purposes, and I would advise against using it for critical database requirements unless it's intended for similar small-scale and experimental projects.

### stupidDB

The dumbest PoC db I use for toy development. Not really actually a database, more of a python wrapper for a json file.

### Command Reference
```bash
just format  # runs black + isort
just lint  # runs mypy + ruff
just test  # runs tests
```

## Setup

### Install [Just](https://github.com/casey/just)
```bash
brew install just  # if you want to use brew (recommended + easier)
```

### Install [Pyenv](https://github.com/pyenv/pyenv) - (optional but recommended)
```bash
pyenv install 3.11.7
pyenv local 3.11.7
```

### Install [Poetry](https://python-poetry.org/docs/)

## Running the project
```bash
# after installing poetry run the following to install dev dependencies
poetry install --with dev --no-root
# if you're using vscode and want the venv path to python for IDE features
poetry run which python  # copy the output of this command and paste it into your .vscode/settings.json {"python.defaultInterpreterPath": PATH}
just test  # runs tests
```

## FAQ

If any questions are ever asked, they will be answered here. 🙋

## License

[GPL-3](https://choosealicense.com/licenses/gpl-3.0/)
