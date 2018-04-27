from ._client import send


def roots(endpoint, database_id=None, pagesize=None):
    url = endpoint + '/namespace/root/page'
    params = {'id': database_id, 'pageSize': pagesize}
    return send(url, 'GET', **params)


def info(endpoint, namespace):
    url = endpoint + '/namespace'
    params = {'namespace': namespace}
    return send(url, 'GET', **params)


def mosaic_definitions(endpoint, namespace, database_id=None, pagesize=None):
    url = endpoint + '/namespace/mosaic/definition/page'
    params = {'namespace': namespace, 'id': database_id, 'pageSize': pagesize}
    return send(url, 'GET', **params)
