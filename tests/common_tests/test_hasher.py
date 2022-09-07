import unittest
import random


from common import hasher


class TestNumberToBytes(unittest.TestCase):

    def test_zero(self):
        res = hasher._number_to_bytes(0)
        self.assertEqual(res, b"\x00")

    def test_pos_neg(self):
        num = random.randint(1, 1000)
        pos = hasher._number_to_bytes(num)
        neg = hasher._number_to_bytes(-num)
        self.assertEqual(pos, neg, f"failed for {num}")

    def test_one_byte_01(self):
        res = hasher._number_to_bytes(1)
        self.assertEqual(res, b"\x01")

    def test_one_byte_02(self):
        res = hasher._number_to_bytes(64)
        self.assertEqual(res, b"\x40")

    def test_one_byte_03(self):
        res = hasher._number_to_bytes(255)
        self.assertEqual(res, b"\xff")

    def test_two_bytes_01(self):
        res = hasher._number_to_bytes(256)
        self.assertEqual(res, b"\x01\x00")

    def test_two_bytes_02(self):
        res = hasher._number_to_bytes(2048)
        self.assertEqual(res, b"\x08\x00")

    def test_two_bytes_03(self):
        res = hasher._number_to_bytes(2056)
        self.assertEqual(res, b"\x08\x08")

    def test_two_bytes_04(self):
        res = hasher._number_to_bytes(65535)
        self.assertEqual(res, b"\xff\xff")


class TestMakeHash(unittest.TestCase):

    def setUp(self):
        self.sample_text = """
GET
webservices.amazon.com
/onca/xml
AWSAccessKeyId=00000000000000000000&ItemId=0679722769&Operation=ItemLookup&ResponseGroup=ItemAttributes%2COffers%2CImages%2CReviews&Service=AWSECommerceService&Timestamp=2009-01-01T12%3A00%3A00Z&Version=2009-01-06
                               """.strip()
        self.sample_hash = "Nace+U3Az4OhN7tISqgs1vdLBHBEijWcBeCqL5xN9xg"
        self.empty_message_hash = "thNnmggU2ex3L5XXeMNfxf8Wl8STcVZTxscSFEKSxa0"

    def test_no_key(self):
        res = hasher.make_hash(self.sample_text)
        self.assertEqual(res, self.sample_hash)

    def test_with_string_key(self):
        res = hasher.make_hash(self.sample_text, hasher.DEFAULT_HASH_KEY.decode())
        self.assertEqual(res, self.sample_hash)

    def test_with_bytes_key(self):
        res = hasher.make_hash(self.sample_text, hasher.DEFAULT_HASH_KEY)
        self.assertEqual(res, self.sample_hash)


    def test_empty_01(self):
        res = hasher.make_hash("", "")
        self.assertEqual(res, self.empty_message_hash)

    def test_empty_02(self):
        res = hasher.make_hash("", b"")
        self.assertEqual(res, self.empty_message_hash)

    def test_empty_03(self):
        res = hasher.make_hash("", 0)
        self.assertEqual(res, self.empty_message_hash)


class TestMakeIdHash(unittest.TestCase):

    def test_zero(self):
        res = hasher.make_id_hash(0, 0)
        self.assertEqual(res, "ZiCzHykkuMAVR3RfQYJdMiM2+D67E9cjZ4eJ1VTYo+8")


if __name__ == '__main__':
    unittest.main()
