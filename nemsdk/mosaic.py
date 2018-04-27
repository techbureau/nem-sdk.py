from nemsdk.com.requests.namespace import mosaic_definitions
from nemsdk.network import get_random_endpoint


MAX_MOSAIC_QUANTITY = 9000000000000000

XEM_SUPPLY = 8999999999


XEM_DIVISIBILITY = 6


def create_attachment(namespace_id, mosaic_name, quantity, initial_supply=None, divisibility=None):
    return {
        "mosaicId": {
            "namespaceId": namespace_id,
            "name": mosaic_name,
        },
        "quantity": quantity,
        "initialSupply": initial_supply,
        "divisibility": divisibility,
    }


class Mosaic:
    def __init__(self, namespace_id, name,
                 divisibility=None, mutable=None, initial_supply=None, transferable=None, levy=None):

        self.namespace_id = namespace_id
        self.name = name
        self.divisibility = divisibility
        self.mutable = mutable
        self.initial_supply = initial_supply
        self.transferable = transferable
        self.levy = levy

    def request_self(self, endpoint='random'):
        ep = get_random_endpoint() if endpoint == 'random' else endpoint
        mosaics = mosaic_definitions(ep, self.namespace_id)['data']
        mosaic = next(filter(lambda m: m['mosaic']['id']['name'] == self.name, mosaics), None)

        if not mosaic:
            raise KeyError('mosaic `{} * {}` is not found'.format(self.namespace_id, self.name))

        self.levy = mosaic['mosaic']['levy']
        properties = mosaic['mosaic']['properties']
        self.divisibility = int(next(filter(lambda p: p['name'] == 'divisibility', properties), None)['value'])
        self.initial_supply = int(next(filter(lambda p: p['name'] == 'initialSupply', properties), None)['value'])
        self.transferable = next(filter(lambda p: p['name'] == 'transferable', properties), None)['value']

    def prepare_as_attachment(self, quantity):
        entity = {
            "mosaicId": {
                "namespaceId": self.namespace_id,
                "name": self.name,
            },
            "quantity": quantity,
            "initialSupply": self.initial_supply,
            "divisibility": self.divisibility,
        }
        return entity


class Xem(Mosaic):
    def __init__(self):
        super().__init__(
            namespace_id='nem', name='xem', initial_supply=XEM_SUPPLY,
            divisibility=XEM_DIVISIBILITY, mutable=False, transferable=True, levy=None
        )
