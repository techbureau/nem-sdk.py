import unittest
from unittest.mock import patch
from nemsdk.com.requests import transaction


@patch('nemsdk.com.requests.transaction.send')
class TestNisState(unittest.TestCase):
    _endpoint = 'http://endpoint:7890'
    _request_announced_obj = {'data': 'data', 'signature': 'sig'}

    def test_announce(self, mock):
        transaction.announce(self._endpoint, self._request_announced_obj)
        expected_endpoint = '{}/transaction/announce'.format(self._endpoint)
        mock.assert_called_with(expected_endpoint, 'POST', data='data', signature='sig')


if __name__ == '__main__':
    unittest.main()
