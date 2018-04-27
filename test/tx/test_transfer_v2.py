import unittest
from unittest.mock import patch
from nemsdk.tx import TransferTx2
from nemsdk.tx_type import *
from nemsdk.tx_version import *
from nemsdk.crypto.key_pair import get_random_account
from nemsdk.mosaic import create_attachment


class TestTransferTx1(unittest.TestCase):
    def setUp(self):
        self.subject = TransferTx2
        self.my_sk, self.my_pk, self.my_address = get_random_account()
        self.your_sk, self.your_pk, self.your_address = get_random_account()

    def test_transaction_version(self):
        self.assertEqual(self.subject.Tx_v, TWO)

    def test_transaction_type(self):
        self.assertEqual(self.subject.Type, TRANSFER)

    def test_message_type(self):
        amount = 'amount'
        mosaics = 'mosaics'
        messages = ('not dict', {'type': 1, 'not payload': 'msg'}, {'not type': 1, 'payload': 'msg'})
        for msg in messages:
            with self.assertRaises(AssertionError):
                self.subject(self.your_address, self.my_pk, mosaics, amount=amount, message=msg)

        correct_message = {'type': 1, 'payload': 'msg'}
        self.subject(self.your_address, self.my_pk, mosaics, amount=amount, message=correct_message)

    def test_prepare(self):
        with patch.object(self.subject, '_prepare_timestamp', return_value='timestamp_value'), \
             patch.object(self.subject, '_prepare_amount', return_value='amount_value'), \
             patch.object(self.subject, '_prepare_fee', return_value='fee_value'), \
             patch.object(self.subject, '_prepare_deadline', return_value='deadline_value'), \
             patch.object(self.subject, '_prepare_version', return_value='version_value'):

            amount = 'amount'  # has no meaning
            message = {'type': 1, 'payload': 'message'}
            mosaic = create_attachment('nem', 'xem', 100000)
            mosaic['dummy'] = 'dummy_value'

            tx = self.subject(self.your_address, self.my_pk, mosaics=mosaic, amount=amount, message=message)
            entity_expected = {
                "timeStamp": 'timestamp_value',
                "amount": 'amount_value',
                "fee": 'fee_value',
                "recipient": self.your_address,
                "type": TRANSFER,
                "deadline": 'deadline_value',
                "message": {'type': 1, 'payload': 'message'},
                "version": 'version_value',
                "signer": self.my_pk,
                "mosaics": [{
                    "mosaicId": {
                        "namespaceId": "nem",
                        "name": "xem"
                    },
                    "quantity": 100000,
                }]
            }
            self.assertDictEqual(tx.prepare(), entity_expected)

    def test_prepare_amount(self):
        with patch('nemsdk.tx.to_micro_xem') as mock_method:
            mosaic = 'mosaic'
            amount = 1234
            tx = self.subject(self.your_address, self.my_pk, mosaic, amount=amount)
            tx._prepare_amount()
            mock_method.assert_called_once_with(amount)

    def test_prepare_fee(self):
        with patch('nemsdk.tx.fee') as fee, patch('nemsdk.tx.to_micro_xem') as to_micro_xem:
            amount = 'amount'
            message = {'type': 1, 'payload': 'message'}
            mosaics = ['mosaics']

            tx = self.subject(self.your_address, self.my_pk, mosaics, message=message, amount=amount)
            tx._prepare_fee()

            fee.transfer.assert_called_once_with(amount, message, mosaics)
            to_micro_xem.assert_called_once_with(fee.transfer())


if __name__ == '__main__':
    unittest.main()
