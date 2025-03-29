import unittest
import os
import sqlite3
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import init_db, DB_PATH

class Testdatabase(unittest.TestCase):

    def setUp(self):
        # Remove the database file if it exists
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def tearDown(self):
        #Clean up after tests
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_database_creation(self):
        #Test database creation
        init_db()
        self.assertTrue(os.path.exists(DB_PATH), f"Database file {DB_PATH} was not created.")

    def test_table_creation(self):
        #Test if the 'shared_data' table is created.
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shared_data';")
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result, "Table 'shared_data' was not created.")

    def test_multiple_initializations(self):
        #Test that calling init_db multiple times doesn't create duplicate tables.
        init_db()
        init_db()  # 2nd initializatino
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='shared_data';")
        result = cursor.fetchone()
        conn.close()
        self.assertEqual(result[0], 1, "The 'shared_data' table was created more than once.")

    def test_table_columns(self):
        #Test if the 'shared_data' table has the correct columns.
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(shared_data);")
        columns = [column[1] for column in cursor.fetchall()]
        conn.close()
        expected_columns = ['id', 'username', 'session_url', 'trial_name', 'email']
        self.assertEqual(columns, expected_columns, f"Columns don't match: {columns}")

if __name__ == "__main__":
    unittest.main()
