import json
from os import remove
from os.path import exists
from typing import Any


class StupidDB:
    def __init__(self, path: str = "db.json") -> None:
        self.path = path
        self.local_db: list[dict] = []
        if not exists(path):
            self.write_to_db()
        self.refresh_db()

    def refresh_db(self) -> None:
        try:
            with open(self.path, "r") as f:
                self.local_db = json.load(f)
        except (FileNotFoundError, PermissionError) as e:
            raise FileNotFoundError(f"Error reading from {self.path}: {e}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error deserializing JSON: {e}")
        except (UnicodeDecodeError, OSError, IOError) as e:
            raise IOError(f"File I/O error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def write_to_db(self) -> None:
        try:
            with open(self.path, "w") as f:
                json.dump(self.local_db, f)
        except (FileNotFoundError, PermissionError) as e:
            raise FileNotFoundError(f"Error reading from {self.path}: {e}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error deserializing JSON: {e}")
        except (UnicodeEncodeError, OSError, IOError) as e:
            raise IOError(f"File I/O error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def delete_db(self) -> None:
        self.local_db = []
        remove(self.path)

    def insert(self, data: Any) -> None:
        """
        Insert data into the database.
        """
        self.refresh_db()
        self.local_db.append(data)
        self.write_to_db()

    def update(self, index: int, data: Any) -> None:
        """
        Update data at the given index.
        """
        self.refresh_db()
        try:
            self.local_db[index] = data
        except IndexError:
            raise IndexError("Index out of range")
        self.write_to_db()

    def retrieve(self, index: int) -> Any:
        """
        Retrieve data from the given index.
        """
        self.refresh_db()
        try:
            return self.local_db[index]
        except IndexError:
            raise IndexError("Index out of range")

    def remove(self, index: int) -> None:
        """
        Remove data at the given index.
        """
        self.refresh_db()
        try:
            self.local_db.pop(index)
            self.write_to_db()
        except IndexError:
            raise IndexError("Index out of range")
