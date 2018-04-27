import unittest
from unittest.mock import patch
from nemsdk.tx import TransferTx1
from nemsdk.tx_type import *
from nemsdk.tx_version import *
from nemsdk.crypto.key_pair import get_random_account


class TestTransferTx1(unittest.TestCase):
    def setUp(self):
        self.subject = TransferTx1
        self.my_sk, self.my_pk, self.my_address = get_random_account()
        self.your_sk, self.your_pk, self.your_address = get_random_account()

    def test_transaction_version(self):
        self.assertEqual(self.subject.Tx_v, ONE)

    def test_transaction_type(self):
        self.assertEqual(self.subject.Type, TRANSFER)

    def test_message_type(self):
        amount = 'amount'

        messages = ('not dict', {'type': 1, 'not payload': 'msg'}, {'not type': 1, 'payload': 'msg'})
        for msg in messages:
            with self.assertRaises(AssertionError):
                self.subject(amount, recipient=self.your_address, signer=self.my_pk, message=msg)

        correct_message = {'type': 1, 'payload': 'msg'}
        self.subject(amount, recipient=self.your_address, signer=self.my_pk, message=correct_message)

    def test_prepare(self):
        with patch.object(self.subject, '_prepare_timestamp', return_value='timestamp_value'), \
             patch.object(self.subject, '_prepare_amount', return_value='amount_value'), \
             patch.object(self.subject, '_prepare_fee', return_value='fee_value'), \
             patch.object(self.subject, '_prepare_deadline', return_value='deadline_value'), \
             patch.object(self.subject, '_prepare_version', return_value='version_value'):

            amount = 'amount'  # has no meaning
            message = {'type': 1, 'payload': 'message'}

            tx = self.subject(amount, recipient=self.your_address, signer=self.my_pk, message=message)
            entity_expected = {
                "timeStamp": 'timestamp_value',
                "amount": 'amount_value',
                "fee": 'fee_value',
                "recipient": self.your_address,
                "type": TRANSFER,
                "deadline": 'deadline_value',
                "message": {'type': 1, 'payload': 'message'},
                "version": 'version_value',
                "signer": self.my_pk
            }
            self.assertDictEqual(tx.prepare(), entity_expected)

    def test_prepare_amount(self):
        with patch('nemsdk.tx.to_micro_xem') as mock_method:
            amount = 1234
            tx = self.subject(amount, self.your_address, self.my_pk)
            tx._prepare_amount()
            mock_method.assert_called_once_with(amount)

    def test_prepare_fee(self):
        with patch('nemsdk.tx.fee') as fee, patch('nemsdk.tx.to_micro_xem') as to_micro_xem:
            amount = 'amount'
            message = {'type': 1, 'payload': 'message'}

            tx = self.subject(amount, self.your_address, self.my_pk, message=message)
            tx._prepare_fee()

            fee.transfer.assert_called_once_with(amount, message)
            to_micro_xem.assert_called_once_with(fee.transfer())


if __name__ == '__main__':
    unittest.main()
