import unittest

from pathlib import Path
import shutil
import tempfile
import sqlite3


from common import database


class TestSqliteDatabase(unittest.TestCase):

    def setUp(self):
        self.scratch_path = Path(tempfile.mkdtemp())
        self.database_file = self.scratch_path / "database.tst"

    def tearDown(self):
        shutil.rmtree(self.scratch_path)

    def test_no_database_01(self):
        database_path = self.scratch_path / "does-not-exist"
        with self.assertRaises(database.DatabaseError):
            database.Database(database_path)

    def test_no_database_02(self):
        database_path = self.scratch_path / "does-not-exist"
        db = database.Database(database_path, False)
        self.assertEqual(db.database_path, database_path)

    def test_connect_01(self):
        db = database.Database(self.database_file, False)
        self.assertIsNone(db.connection)
        db.connect()
        self.assertIsNotNone(db.connection)
        with self.assertRaises(database.DatabaseError):
            db.connect()

    def test_disconnect_01(self):
        db = database.Database(self.database_file, False)
        self.assertIsNone(db.connection)
        with self.assertRaises(database.DatabaseError):
            db.disconnect()

    def test_disconnect_02(self):
        db = database.Database(self.database_file, False)
        db.connect()
        self.assertIsNotNone(db.connection)
        db.disconnect()
        self.assertIsNone(db.connection)

    def test_cursor_01(self):
        db = database.Database(self.database_file, False)
        with self.assertRaises(database.DatabaseError):
            db.cursor()

    def test_cursor_02(self):
        db = database.Database(self.database_file, False)
        db.connect()
        c = db.cursor()
        self.assertIsInstance(c, sqlite3.Cursor)
        db.disconnect()

    def test_context_01(self):
        with database.Database(self.database_file, False) as db:
            self.assertIsNotNone(db.connection)

    def test_context_02(self):
        with database.Database(self.database_file, False) as db:
            with self.assertRaises(database.DatabaseError):
                db.connect()

    def test_context_03(self):
        with self.assertRaises(RuntimeError):
            with database.Database(self.database_file, False) as db:
                self.assertIsNotNone(db.connection)
                raise RuntimeError("TEST")
            self.assertIsNone(db.connection)


if __name__ == '__main__':
    unittest.main()
