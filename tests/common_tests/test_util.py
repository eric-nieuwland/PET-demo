import unittest

import os
import tempfile
import shutil


from common import util


class TestMakeDatabasePath(unittest.TestCase):

    def tearDown(self):
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
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
        p, f = os.path.split(res)
        self.assertTrue(f, "test.db")
        _, d = os.path.split(p)
        self.assertTrue(d, "database")


if __name__ == '__main__':
    unittest.main()
