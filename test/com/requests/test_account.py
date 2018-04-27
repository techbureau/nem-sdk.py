import unittest
from nemsdk.com.requests import account
from unittest.mock import patch


@patch('nemsdk.com.requests.account.send')
class TestAccount(unittest.TestCase):
    _endpoint = 'http://com:7890'
    _address = 'address'
    _public_key = 'public_key'
    _txhash = 'hash'
    _txid = 'id'
    _private_key = 'private_key'
    _parent = 'parent'

    @classmethod
    def _default_path(cls):
        return cls._endpoint + '/account'

    def test_data(self, mock_client):
        account.data(self._endpoint, self._address)
        expected_endpoint = self._default_path() + '/get'
        mock_client.assert_called_with(expected_endpoint, 'GET', address=self._address)

    def test_data_from_public_key(self, mock):
        account.data_from_public_key(self._endpoint, self._public_key)
        expected_endpoint = self._default_path() + '/get/from-public-key'
        mock.assert_called_with(expected_endpoint, 'GET', publicKey=self._public_key)

    def test_forwarded(self, mock):
        account.forwarded(self._endpoint, self._address)
        expected_endpoint = self._default_path() + '/get/forwarded'
        mock.assert_called_with(expected_endpoint, 'GET', address=self._address)

    def forwarded_from_public_key(self, mock):
        account.forwarded(self._endpoint, self._address)
        expected_endpoint = self._default_path() + '/get/forwarded/from-public-key'
        mock.assert_called_with(expected_endpoint, 'GET', publicKey=self._public_key)

    def test_status(self, mock):
        account.status(self._endpoint, self._address)
        expected_endpoint = self._default_path() + '/status'
        mock.assert_called_with(expected_endpoint, 'GET', address=self._address)

    def test_incoming_transactions(self, mock):
        account.incoming_transactions(self._endpoint, self._address, self._txhash, self._txid)
        expected_endpoint = self._default_path() + '/transfers/incoming'
        mock.assert_called_with(expected_endpoint,'GET', address=self._address,
                                hash=self._txhash, id=self._txid)

    def test_outgoing_transactions(self, mock):
        account.outgoing_transactions(self._endpoint, self._address, self._txhash, self._txid)
        expected_endpoint = self._default_path() + '/transfers/outgoing'
        mock.assert_called_with(expected_endpoint,'GET', address=self._address,
                                hash=self._txhash, id=self._txid)

    def test_all_transactions(self, mock):
        account.all_transactions(self._endpoint, self._address, self._txhash, self._txid)
        expected_endpoint = self._default_path() + '/transfers/all'
        mock.assert_called_with(expected_endpoint,'GET', address=self._address,
                                hash=self._txhash, id=self._txid)

    def test_unconfirmed_transactions(self, mock):
        account.unconfirmed_transactions(self._endpoint, self._address)
        expected_endpoint = self._default_path() + '/unconfirmedTransactions'
        mock.assert_called_with(expected_endpoint,'GET', address=self._address)

    def test_harvested_blocks(self, mock):
        account.harvested_blocks(self._endpoint, self._address)
        expected_endpoint = self._default_path() + '/harvests'
        mock.assert_called_with(expected_endpoint, 'GET', address=self._address)

    def test_namespaces_owned(self, mock):
        account.namespaces_owned(self._endpoint, self._address, self._parent)
        expected_endpoint = self._default_path() + '/namespace/page'
        mock.assert_called_with(expected_endpoint, 'GET', address=self._address, parent=self._parent)

    def test_mosaic_definitions_created(self, mock):
        account.mosaic_definitions_created(self._endpoint, self._address, self._parent)
        expected_endpoint = self._default_path() + '/mosaic/definition/page'
        mock.assert_called_with(expected_endpoint, 'GET', address=self._address, parent=self._parent)

    def test_mosaic_definitions(self, mock):
        account.mosaic_definitions(self._endpoint, self._address)
        expected_endpoint = self._default_path() + '/mosaic/owned/definition'
        mock.assert_called_with(expected_endpoint, 'GET', address=self._address)

    def test_mosaic_owned(self, mock):
        account.mosaic_owned(self._endpoint, self._address)
        expected_endpoint = self._default_path() + '/mosaic/owned'
        mock.assert_called_with(expected_endpoint, 'GET', address=self._address)

    def test_unlock_info(self, mock):
        account.unlock_info(self._endpoint)
        expected_endpoint = self._default_path() + '/unlocked/info'
        mock.assert_called_with(expected_endpoint, 'POST')

    def test_start_harvesting(self, mock):
        account.start_harvesting(self._endpoint, self._private_key)
        expected_endpoint = self._default_path() + '/unlock'
        mock.assert_called_with(expected_endpoint, 'POST', value=self._private_key)

    def test_stop_harvesting(self, mock):
        account.stop_harvesting(self._endpoint, self._private_key)
        expected_endpoint = self._default_path() + '/lock'
        mock.assert_called_with(expected_endpoint, 'POST', value=self._private_key)

    def test_historical_data(self, mock):
        startheight, endheight, increment = 1, 10, 1
        account.historical_data(self._endpoint, self._address, startheight, endheight, increment)
        expected_endpoint = self._default_path() + '/historical/get'
        mock.assert_called_with(expected_endpoint, 'GET', address=self._address,
                                startHeight=startheight, endHeight=endheight, increment=increment)


if __name__ == '__main__':
    unittest.main()
