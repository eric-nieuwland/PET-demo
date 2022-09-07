import unittest

from pathlib import Path
import shutil


from common import util


class TestMakeDatabasePath(unittest.TestCase):

    def tearDown(self):
        db_path = Path(__file__).parent.parent / "database"
        shutil.rmtree(db_path, ignore_errors=True)

    def test_non_string(self):
        with self.assertRaises(TypeError):
            util.make_database_path(1)
        with self.assertRaises(TypeError):
            util.make_database_path([])
        with self.assertRaises(TypeError):
            util.make_database_path(None)

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            util.make_database_path("")

    def test_non_database_path(self):
        res = util.make_database_path("test.py")
        self.assertIsInstance(res, Path)
        f = res.name
        self.assertTrue(f, "test.db")
        d = res.parent
        self.assertTrue(d, "database")


if __name__ == '__main__':
    unittest.main()
