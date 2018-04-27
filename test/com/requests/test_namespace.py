import unittest
from unittest.mock import patch
from nemsdk.com.requests import namespace


@patch('nemsdk.com.requests.namespace.send')
class TestNisState(unittest.TestCase):
    _endpoint = 'http://com:7890'
    _namespace = 'namespace'
    _database_id = 'id'
    _pagesize = 20

    def test_roots(self, mock):
        namespace.roots(self._endpoint, self._database_id, self._pagesize)
        expected_endpoint = '{}/namespace/root/page'.format(self._endpoint)
        mock.assert_called_with(expected_endpoint, 'GET', id=self._database_id, pageSize=self._pagesize)

    def test_info(self, mock):
        namespace.info(self._endpoint, self._namespace)
        expected_endpoint = '{}/namespace'.format(self._endpoint)
        mock.assert_called_with(expected_endpoint, 'GET', namespace=self._namespace)

    def test_mosaic_definitions(self, mock):
        namespace.mosaic_definitions(self._endpoint, self._namespace, self._database_id, self._pagesize)
        expected_endpoint = '{}/namespace/mosaic/definition/page'.format(self._endpoint)
        mock.assert_called_with(expected_endpoint, 'GET', namespace=self._namespace, id=self._database_id, pageSize=self._pagesize)


if __name__ == '__main__':
    unittest.main()
