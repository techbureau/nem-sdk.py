import unittest
from unittest.mock import patch
from nemsdk.com.requests import node


@patch('nemsdk.com.requests.node.send')
class TestNisState(unittest.TestCase):
    _endpoint = 'http://com:7890'
    _blockhash = 'hash'
    _blockheight = 300

    def test_info(self, mock):
        node.info(self._endpoint)
        mock.assert_called_with('{}/node/info'.format(self._endpoint), 'GET')

    def test_extended_info(self, mock):
        node.extended_info(self._endpoint)
        mock.assert_called_with('{}/node/extended-info'.format(self._endpoint), 'GET')

    def test_all_peers(self, mock):
        node.all_peers(self._endpoint)
        mock.assert_called_with('{}/node/peer-list/all'.format(self._endpoint), 'GET')

    def test_reachable_peers(self, mock):
        node.reachable_peers(self._endpoint)
        mock.assert_called_with('{}/node/peer-list/reachable'.format(self._endpoint), 'GET')

    def test_active_peers(self, mock):
        node.active_peers(self._endpoint)
        mock.assert_called_with('{}/node/peer-list/active'.format(self._endpoint), 'GET')

    def test_max_chain_height_of_active_peers(self, mock):
        node.max_chain_height_of_active_peers(self._endpoint)
        mock.assert_called_with('{}/node/active-peers/max-chain-height'.format(self._endpoint), 'GET')

    def test_experiences(self, mock):
        node.experiences(self._endpoint)
        mock.assert_called_with('{}/node/experiences'.format(self._endpoint), 'GET')


if __name__ == '__main__':
    unittest.main()
