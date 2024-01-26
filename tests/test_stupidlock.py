import json
import os

import pytest

from stupiddb import StupidLock

lock_test_path = "test_lock.json"


class TestStupidLock:
    @classmethod
    def teardown_class(cls):
        # Clean up the temporary lock file after testing
        if os.path.exists(lock_test_path):
            os.remove(lock_test_path)

    def test_initial_state(self):
        lock = StupidLock(lock_test_path)
        assert lock.is_locked() is False  # The lock should be initially unlocked

    def test_lock_acquire_release(self):
        lock = StupidLock(lock_test_path)

        # Acquire the lock
        lock.acquire_lock()

        # Check if the lock is acquired
        assert lock.is_locked() is True

        # Release the lock
        lock.release_lock()

        # Check if the lock is released
        assert lock.is_locked() is False

    def test_lock_file_contents(self):
        lock = StupidLock(lock_test_path)

        # Acquire the lock
        lock.acquire_lock()

        # Check the contents of the lock file
        with open(lock_test_path, "r") as f:
            lock_data = json.load(f)
            assert lock_data[lock.LOCK_FILE_KEY] == lock.LOCK_FILE_LOCKED

        # Release the lock
        lock.release_lock()

        # Check the contents of the lock file after release
        with open(lock_test_path, "r") as f:
            lock_data = json.load(f)
            assert lock_data[lock.LOCK_FILE_KEY] == lock.LOCK_FILE_UNLOCKED

    def test_lock_timeout(self):
        lock = StupidLock(lock_test_path)

        # Acquire the lock
        assert lock.acquire_lock() is True

        _lock = StupidLock(lock_test_path)
        assert _lock.is_locked() is True

        pytest.raises(TimeoutError, _lock.acquire_lock)

        assert _lock.is_locked() is True
