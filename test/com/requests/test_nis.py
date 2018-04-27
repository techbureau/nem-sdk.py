import unittest
from unittest.mock import patch
from nemsdk.com.requests import nis


@patch('nemsdk.com.requests.nis.send')
class TestNisState(unittest.TestCase):
    _endpoint = 'http://com:7890'

    def test_heart_beat(self, mock):
        nis.heartbeat(self._endpoint)
        mock.assert_called_with('{}/heartbeat'.format(self._endpoint), 'GET')

    def test_status(self, mock):
        nis.status(self._endpoint)
        mock.assert_called_with('{}/status'.format(self._endpoint), 'GET')


if __name__ == '__main__':
    unittest.main()
