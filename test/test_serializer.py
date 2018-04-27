import unittest
from nemsdk.serializer import serialize_tx


class TestSerializer(unittest.TestCase):
    def test_tx1(self):
        pass

    def test_tx2(self):
        entity = {
            'amount': 1000000,
            'fee': 450000,
            'recipient': 'NCY7LJBP24EJJARCI2TGK72WQ4UNRV2GX6HLOG7A',
            'type': 257,
            'message': None,
            'mosaics': [{'quantity': 1, 'mosaicId': {'name': 'coin', 'namespaceId': 'test'}}],
            'signer': 'e991dd1b31068cde969a839c813a89b226597573f2f3a360315c93adfc65c75d',
            'timeStamp': 97051703,
            'deadline': 97055303,
            'version': 1744830466
        }

        serialized_tx = serialize_tx(entity)
        expected = '010100000200006837e4c80520000000e991dd1b31068cde969a839c813a89b226597573f2f3a360315c93adfc65c' \
                   '75dd0dd06000000000047f2c805280000004e4359374c4a42503234454a4a415243493254474b373257513455' \
                   '4e525632475836484c4f47374140420f000000000000000000010000001c0000001000000004000000746573740' \
                   '4000000636f696e0100000000000000'

        self.assertEqual(serialized_tx, expected)

        entity2 = {
            'mosaics': [{'mosaicId': {'name': 'samurai', 'namespaceId': 'mijin'}, 'quantity': 100}],
            'version': 1744830466, 'timeStamp': 97052112, 'deadline': 97055712, 'fee': 650000,
            'signer': 'e991dd1b31068cde969a839c813a89b226597573f2f3a360315c93adfc65c75d',
            'message': {'type': 2, 'payload': '9e76586b6d3260541af8815c356ac7e3b40a52a50f9b6811562aa97e3dd924566dcb504a677635c8adcca9657c6bea25c1b56f1c2031d23f2967a5db67b14d9dc23977302c316fa2eef9b7a11c468707'},
            'amount': 1000000,
            'recipient': 'NCY7LJBP24EJJARCI2TGK72WQ4UNRV2GX6HLOG7A',
            'type': 257
        }
        serialized_tx2 = serialize_tx(entity2)
        expected2 = '0101000002000068d0e5c80520000000e991dd1b31068cde969a839c813a89b226597573f2f3a36' \
                   '0315c93adfc65c75d10eb090000000000e0f3c805280000004e4359374c4a42503234454a4a41524' \
                   '3493254474b3732575134554e525632475836484c4f47374140420f0000000000580000000200000' \
                   '0500000009e76586b6d3260541af8815c356ac7e3b40a52a50f9b6811562aa97e3dd924566dcb504' \
                   'a677635c8adcca9657c6bea25c1b56f1c2031d23f2967a5db67b14d9dc23977302c316fa2eef9b7a1' \
                   '1c468707010000002000000014000000050000006d696a696e0700000073616d757261696400000000000000'

        self.assertEqual(serialized_tx2, expected2)

        entity3 = {
            'amount': 1000000,
            'fee': 450000,
            'recipient': 'NCY7LJBP24EJJARCI2TGK72WQ4UNRV2GX6HLOG7A',
            'type': 257,
            'message': None,
            'mosaics': [
                {'quantity': 1, 'mosaicId': {'name': 'sushi', 'namespaceId': 'food'}},
                {'quantity': 12, 'mosaicId': {'name': 'yakiniku', 'namespaceId': 'food'}},
                {'quantity': 15, 'mosaicId': {'name': 'python', 'namespaceId': 'language'}},
                {'quantity': 100, 'mosaicId': {'name': 'ruby', 'namespaceId': 'test'}},
            ],
            'signer': 'e991dd1b31068cde969a839c813a89b226597573f2f3a360315c93adfc65c75d',
            'timeStamp': 97051703,
            'deadline': 97055303,
            'version': 1744830466
        }

        serialized_tx3 = serialize_tx(entity3)
        expected3 = '010100000200006837e4c80520000000e991dd1b31068cde969a839c813a89b226597573f2f3a360315c' \
                   '93adfc65c75dd0dd06000000000047f2c805280000004e4359374c4a42503234454a4a41524349325447' \
                   '4b3732575134554e525632475836484c4f47374140420f000000000000000000040000001d000000110000' \
                   '0004000000666f6f640500000073757368690100000000000000200000001400000004000000666f6f64080' \
                   '0000079616b696e696b750c000000000000002200000016000000080000006c616e677561676506000000707' \
                   '974686f6e0f000000000000001c00000010000000040000007465737404000000727562796400000000000000'

        self.assertEqual(serialized_tx3, expected3)

    def test_multisig(self):
        pass


if __name__ == '__main__':
    unittest.main()
