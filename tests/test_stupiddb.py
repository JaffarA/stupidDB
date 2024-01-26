import json
import os

from stupiddb import StupidDB
import pytest

db_test_path = "test_db.json"


class TestStupidDB:
    @classmethod
    def teardown_class(cls) -> None:
        # Clean up the temporary DB file after testing
        if os.path.exists(db_test_path):
            os.remove(db_test_path)

    def test_init(self) -> None:
        db = StupidDB(db_test_path)
        assert db

    def test_refresh_db(self):
        # Create a test DB file with sample data
        sample_data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        with open(db_test_path, "w") as f:
            json.dump(sample_data, f)

        # Initialize the database and check if it's refreshed correctly
        db = StupidDB(db_test_path)
        assert db.local_db == sample_data

    def test_write_to_db(self):
        # Initialize the database with sample data
        db = StupidDB(db_test_path)
        sample_data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        db.local_db = sample_data

        # Write the data to the test DB file
        db.write_to_db()

        # Read the test DB file and check if it matches the sample data
        with open(db_test_path, "r") as f:
            db_contents = json.load(f)

        assert db_contents == sample_data

    def test_delete_db(self):
        # Initialize the database with sample data
        db = StupidDB(db_test_path)
        sample_data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        db.local_db = sample_data

        # Delete the database
        db.delete_db()

        # Check if the database is empty
        assert db.local_db == []
        assert os.path.exists(db_test_path) is False

    def test_insert_and_retrieve(self):
        # Initialize the database
        db = StupidDB(db_test_path)
        sample_data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        db.local_db = sample_data
        db.write_to_db()

        # Insert a new data entry
        new_entry = {"id": 3, "name": "Charlie"}
        db.insert(new_entry)

        # Retrieve the inserted entry and check if it matches
        retrieved_entry = db.retrieve(
            2
        )  # Index 2 corresponds to the newly inserted entry
        assert retrieved_entry == new_entry

    def test_update(self):
        # Initialize the database with sample data
        db = StupidDB(db_test_path)
        sample_data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        db.local_db = sample_data

        # Update an existing data entry
        updated_entry = {
            "id": 2,
            "name": "Robert",
        }  # Update the "name" field of entry with ID 2
        db.update(1, updated_entry)  # Index 1 corresponds to the entry with ID 2

        # Retrieve the updated entry and check if it matches the updated data
        retrieved_entry = db.retrieve(1)
        assert retrieved_entry == updated_entry

    def test_remove(self):
        # Initialize the database with sample data
        db = StupidDB(db_test_path)
        sample_data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

        db.insert(sample_data[0])
        db.insert(sample_data[1])

        # Remove an existing data entry
        db.remove(1)  # remove 'Bob' entry

        # Check if the entry is removed
        pytest.raises(IndexError, db.retrieve, 1)

        assert db.retrieve(0) == sample_data[0]
