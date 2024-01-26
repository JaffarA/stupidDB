import json
from os.path import exists
from time import sleep


class StupidLock:
    LOCK_FILE_KEY = "loqd"
    LOCK_FILE_UNLOCKED = "0"
    LOCK_FILE_LOCKED = "1"

    def __init__(self, path: str = "lock.json") -> None:
        self.LOCK_FILE = path
        self.locked = True
        if not exists(self.LOCK_FILE):
            with open(self.LOCK_FILE, "w") as f:
                json.dump({self.LOCK_FILE_KEY: self.LOCK_FILE_UNLOCKED}, f)
        self.check_lock()

    def check_lock(self) -> None:
        try:
            self.locked = self.is_locked()
        except json.JSONDecodeError:
            self.release_lock()

    def is_locked(self) -> bool:
        with open(self.LOCK_FILE, "r") as f:
            return json.load(f)[self.LOCK_FILE_KEY] == self.LOCK_FILE_LOCKED

    def acquire_lock(self, iteration: int = 0) -> bool:
        """
        A blocking call to acquire the lock.
        """
        self.check_lock()
        if self.locked:
            if iteration > 100:
                raise TimeoutError("Could not acquire lock")
            sleep(0.05)
            return self.acquire_lock(iteration = iteration + 1)
        self._lock()
        return self.locked

    def release_lock(self) -> None:
        with open(self.LOCK_FILE, "w") as f:
            json.dump({self.LOCK_FILE_KEY: self.LOCK_FILE_UNLOCKED}, f)
        self.check_lock()

    def _lock(self) -> None:
        with open(self.LOCK_FILE, "w") as f:
            json.dump({self.LOCK_FILE_KEY: self.LOCK_FILE_LOCKED}, f)
        self.locked = True
