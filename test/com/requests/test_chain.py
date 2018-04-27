import unittest
from unittest.mock import patch
from nemsdk.com.requests import chain


@patch('nemsdk.com.requests.chain.send')
class TestNisState(unittest.TestCase):
    _endpoint = 'http://com:7890'
    _blockhash = 'hash'
    _blockheight = 300

    def test_height(self, mock):
        chain.height(self._endpoint)
        mock.assert_called_with('{}/chain/height'.format(self._endpoint), 'GET')

    def test_score(self, mock):
        chain.score(self._endpoint)
        mock.assert_called_with('{}/chain/score'.format(self._endpoint), 'GET')

    def test_last_block(self, mock):
        chain.last_block(self._endpoint)
        mock.assert_called_with('{}/chain/last-block'.format(self._endpoint), 'GET')

    def test_block_by_height(self, mock):
        chain.block_by_height(self._endpoint, self._blockheight)
        mock.assert_called_with('{}/block/at/public'.format(self._endpoint), 'POST', height=self._blockheight)


if __name__ == '__main__':
    unittest.main()
