>This project is designed for recreational purposes, and I would advise against using it for critical database requirements unless it's intended for similar small-scale and experimental projects.

### StupidDB

The dumbest PoC db I use for toy development. Not really actually a database, more of a python wrapper for a json file.

Includes two amazingly stupid classes:
- `stupiddb.StupidDB`
    - `insert`
    ```python
    stupiddb.StupidDB().insert(
        {"name": "alice", "age": "21"}
    )
    ```
    - `retrieve`
    ```python
    result = stupiddb.StupidDB().retrieve(
        0  # index of the record to retrieve
    )
    print(result)  # {"name": "alice", "age": "21"}
    ```
    - `update`
    ```python
    stupiddb.StupidDB().update(
        0,  # index of the record to update
        {"name": "alice", "age": "22"}
    )
    ```
    - `remove`
    ```python
    stupiddb.StupidDB().remove(
        0  # index of the record to remove
    )
    ```
- `stupiddb.StupidLock`
    - `is_locked`
    ```python
    stupiddb.StupidLock().is_locked()  # False
    ```
    - `acquire_lock`
    ```python
    stupiddb.StupidLock().acquire_lock()
    stupiddb.StupidLock().is_locked()  # True
    ```
    - `release_lock`
    ```python
    stupiddb.StupidLock().release_lock()
    stupiddb.StupidLock().is_locked()  # False
    ```

### Command Reference
```bash
just format  # runs black + isort
just lint  # runs mypy + ruff
just test  # runs tests
just coverage  # prints coverage report (run after tests)
```

### Example Usage
```python
from stupiddb import StupidDB, StupidLock

db_path = "example_db.json"
lock_path = "example_lock.json"


def register_user(user: dict[str, str]) -> bool:
    # initialize db
    stupid_db = StupidDB(db_path)

    # initialize lock
    lock = StupidLock(lock_path)

    try:
        # acquire lock
        lock.acquire_lock()

        # insert user into db
        stupid_db.insert(user)

        # release lock
        lock.release_lock()
    except Exception as e:
        # handle exception
        # ...something went wrong, the user was not registered
        return False

    return True

alice = {"name": "alice", "age": "21"}
alice_is_registered = register_user(alice)
print(alice_is_registered)  # True
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
