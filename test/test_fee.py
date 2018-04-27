import unittest
from nemsdk import fee
from nemsdk.mosaic import XEM_SUPPLY, XEM_DIVISIBILITY


class TestFee(unittest.TestCase):
    def test_inner_transfer(self):

        amounts_fees = [
            [0, 0.05],
            [5000, 0.05],
            [10000, 0.05],
            [15000, 0.05],
            [20000, 0.1],
            [45000, 0.2],
            [45000.123456, 0.2],
            [250000, 1.25],
            [9999999, 1.25]
        ]

        for i in range(len(amounts_fees)):
            with self.subTest(i=i):
                amount = amounts_fees[i][0]
                f = amounts_fees[i][1]
                self.assertEqual(fee._transfer(amount), f)

    def test_inner_message(self):
        payloads_fees = [
            [None, 0],
            ['', 0],
            ['a' * 1, 0.05],
            ['a' * 31, 0.05],
            ['a' * 32, 0.05],
            ['a' * 33, 0.05],
        ]

        for i in range(len(payloads_fees)):
            with self.subTest(i=i):
                p = payloads_fees[i][0]
                f = payloads_fees[i][1]
                self.assertEqual(fee._message(p), f, msg='{} is expected (i={})'.format(f, i))

    def test_inner_mosaic(self):
        entities = [
            {'amount': 1, 'quantity': 1000000, 'initialSupply': 10000, 'divisibility': 0, 'fee': 0.05},
            {'amount': 1, 'quantity': 10000000000, 'initialSupply': 10000, 'divisibility': 0, 'fee': 0.05},
            {'amount': 1, 'quantity': 1000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 0.05},
            {'amount': 1, 'quantity': 19999999999, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 0.05},
            {'amount': 1, 'quantity': 20000000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 0.1},
            {'amount': 1, 'quantity': 29999999999, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 0.1},
            {'amount': 1, 'quantity': 30000000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 0.15},
            {'amount': 1, 'quantity': 39999999999, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 0.15},
            {'amount': 1, 'quantity': 40000000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 0.2},
            {'amount': 1, 'quantity': 249999999999, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 1.2},
            {'amount': 1, 'quantity': 250000000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 1.25},
            {'amount': 1, 'quantity': 300000000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY, 'fee': 1.25},
        ]

        for entity in entities:
            with self.subTest(entity=entity):
                expected_fee = entity.pop('fee')
                amount = entity.pop('amount')
                self.assertEqual(fee._mosaic(amount, entity), expected_fee, msg='{} is expected'.format(expected_fee))

    def test_transfer(self):
        entities = [
            {'amount': 1, 'mosaics': None, 'message': None, 'fee': 0.05},
            {'amount': 20000, 'mosaics': None, 'message': None, 'fee': 0.1},
            {'amount': 20000, 'mosaics': None, 'message': {'type': 1, 'payload': 'a'}, 'fee': 0.15},
            {'amount': 20000, 'mosaics': None, 'message': {'type': 1, 'payload': 'a' * 32}, 'fee': 0.15},
            {'amount': 20000, 'mosaics': None, 'message': {'type': 1, 'payload': 'a' * 32}, 'fee': 0.15},
            {'amount': 1, 'mosaics': {'quantity': 1000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY}, 'message': None, 'fee': 1.25},
            {'amount': 1, 'mosaics': {'quantity': 1000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY}, 'message': {'type': 1, 'payload': 'a'}, 'fee': 1.3},
            {'amount': 1, 'mosaics': {'quantity': 1000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY}, 'message': {'type': 1, 'payload': 'a' * 32}, 'fee': 1.3},
            {'amount': 1,
             'mosaics': [{'quantity': 1000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY}, {'quantity': 1000000, 'initialSupply': 1000, 'divisibility': 1}],
             'message': None, 'fee': 1.4},
            {'amount': 1,
             'mosaics': [{'quantity': 1000000, 'initialSupply': XEM_SUPPLY, 'divisibility': XEM_DIVISIBILITY}, {'quantity': 1000000, 'initialSupply': 1000, 'divisibility': 1}],
             'message': {'type': 1, 'payload': 'あ' * 22}, 'fee': 1.5},
        ]

        for i, entity in enumerate(entities):
            with self.subTest(entity=entity):
                expected_fee = entity.pop('fee')
                amount = entity.pop('amount')
                mosaics = entity.pop('mosaics')
                message = entity.pop('message')
                self.assertEqual(fee.transfer(amount, message, mosaics),
                                 expected_fee, msg='{} is expected (i={})'.format(expected_fee, i))


if __name__ == '__main__':
    unittest.main()
