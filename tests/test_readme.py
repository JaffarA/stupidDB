import os

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
    except Exception:
        # handle exception
        # ...something went wrong, the user was not registered
        return False

    return True


class TestREADME:
    @classmethod
    def teardown_class(cls):
        os.remove(db_path)
        os.remove(lock_path)

    def test_register_user(self):
        alice: dict[str, str] = {"name": "alice", "age": "21"}
        alice_is_registered: bool = register_user(alice)
        assert alice_is_registered is True
