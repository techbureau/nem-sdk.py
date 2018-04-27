import unittest
from nemsdk.tx import MultisigMixIn


class _DummyTransaction(MultisigMixIn):
    network = 'mainnet'

    def prepare(self):
        return {
            'timeStamp': 'current_time',
            'deadline': 'after_two_hours',
            'data': 'some_data',
        }


class TestMultisigTx(unittest.TestCase):
    def setUp(self):
        self.Tx = _DummyTransaction

    def test_prepare_multisig_fee(self):
        tx = self.Tx()
        self.assertEqual(tx._prepare_multisig_fee(), 150000)

    def test_prepare_as_multisig(self):
        tx = self.Tx()
        entity = tx.prepare_as_multisig(issuer='me')

        entity_expected = {
            'timeStamp': 'current_time',
            'fee': 150000,
            'type': 0x1004,
            'deadline': 'after_two_hours',
            'version': 1744830465,
            'signer': 'me',
            'otherTrans': {
                'timeStamp': 'current_time',
                'deadline': 'after_two_hours',
                'data': 'some_data',
            },
            'signatures': []
        }

        self.assertDictEqual(entity, entity_expected)


if __name__ == '__main__':
    unittest.main()
