import unittest


from common import output


class TestOutputCollectDatabaseRows(unittest.TestCase):

    def test_no_rows(self):
        res = output._collect_database_rows([])
        self.assertListEqual(res, [])

    def test_one_row(self):
        row = {'a': 'a', 'b': 1, 'c': None}
        res = output._collect_database_rows([row])
        self.assertEqual(len(res), 2)
        self.assertDictEqual(dict(zip(res[0], res[1])), row)

    def test_two_rows(self):
        rows = [
            {'a': 'a', 'b': 1, 'c': None},
            {'a': 'aap', 'b': 42, 'c': 'MIES'},
        ]
        res = output._collect_database_rows(rows)
        self.assertEqual(len(res), 3)
        self.assertDictEqual(dict(zip(res[0], res[1])), rows[0])
        self.assertDictEqual(dict(zip(res[0], res[2])), rows[1])


class TestOutputComputeColumnWidths(unittest.TestCase):

    def test_no_rows(self):
        with self.assertRaises(IndexError):
            output._compute_column_widths([])

    def test_one_row(self):
        rows = [
            ['h', 'hh', 'hhh'],
        ]
        res = output._compute_column_widths(rows)
        self.assertListEqual(res, [1, 2, 3])

    def test_two_equal_length_rows(self):
        rows = [
            ['aap', 'noot', 'mies'],
            ['eb', 'vloed', 'mist'],
        ]
        res = output._compute_column_widths(rows)
        self.assertListEqual(res, [3, 5, 4])

    def test_two_unequal_length_rows(self):
        rows = [
            ['aap', 'noot', 'mies'],
            ['eb', 'vloed', 'mist', 'regen'],
        ]
        with self.assertRaises(IndexError):
            output._compute_column_widths(rows)


class TestOutputMakeRowFormat(unittest.TestCase):

    def test_no_widths(self):
        res = output._make_row_format([], ["sample"])
        self.assertEqual(res, "|")

    def test_one_width_string(self):
        res = output._make_row_format([6], ["sample"])
        self.assertEqual(res, "| {0:6s} |")

    def test_one_width_int(self):
        res = output._make_row_format([4], [666])
        self.assertEqual(res, "| {0:4d} |")

    def test_one_width_other(self):
        res = output._make_row_format([12], [b""])
        self.assertEqual(res, "| {0!r:^12s} |")

    def test_one_width_no_sample(self):
        with self.assertRaises(IndexError):
            output._make_row_format([12], [])

    def test_three_widths(self):
        res = output._make_row_format([4, 6, 9], ["", 0, b""])
        self.assertEqual(res, "| {0:4s} | {1:6d} | {2!r:^9s} |")


class TestOutputMakeSeparator(unittest.TestCase):

    def test_empty_format(self):
        res = output._make_separator("")
        self.assertEqual(res, "")

    def test_no_argument(self):
        res = output._make_separator("xyz | abc")
        self.assertEqual(res, "xyz-+-abc")

    def test_one_width_01(self):
        res = output._make_separator("| {0} |")
        self.assertEqual(res, "+--+")

    def test_one_width_02(self):
        res = output._make_separator("| {0:3s} |")
        self.assertEqual(res, "+-----+")

    def test_three_widths(self):
        res = output._make_separator("| {0:4s} | {1:6s} | {2:9s} |")
        self.assertEqual(res, "+------+--------+-----------+")


if __name__ == '__main__':
    unittest.main()
