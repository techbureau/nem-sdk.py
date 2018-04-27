# nem-sdk.py(beta)

## Require

Python3 (>=3.5)

Features:
* Simple structure
* NIS API requests
* Sending XEM and Mosaics
* Encrypted, unencrypted messaging
* Example code

Todo:
* Support Websocket
* Support Apostille
* Support Transactions about mosaic

## Example

Characters:

```python
[Nobita]
nobita_secret_key = '98b8f1e9d8aa4ee18576e719385eaa7656ea5eb6750ef29a9d654fe638a23340'
nobita_public_key = '984d1f8f6e58b99d62ec30b37d3c3e3aee89dfe74d253009bf11fbd2997b8877'
nobita_address = 'NBEICAZCPL3SGSIRXO73AG32Q7YKEEGOLR7PSRL7'

[Suneo]
suneo_secret_key = '88fc854a67e1c976b220dec471a54da0828003e54093b3cadec65f594831e664'
suneo_public_key = 'a7e78b2eebfffc4cb9ab42790e00ab602df0bf053543c48afd5f19478a877777'
suneo_address = 'NDADL5VH4WI47UIE3LZGFVWFEBDHF4PL76YQ3EZP'

[Shizuka]
shizuka_secret_key = '305ac4dbc32da5660e5a0d94e5d5d6a5f8d49d4aafb2dbc1af78bc7f039af579'
shizuka_public_key = '72e69b9fce84fd92f476d948c4a20bb61812d71a7847c826e5b23d4d0a6523de'
shizuka_address = 'NDSRH5Q5BI7WBWQJCF5NB4KUDKBRW7TVFY2U3ANM'


endpoint = 'http://alice4.nem.ninja:7890'
```

### Send XEM

Case: send XEM from **Nobita** to **Suneo**

```python
from nemsdk import request
from nemsdk.tx import TransferTx1

tx = TransferTx1(amount=1, recipient=suneo_address, signer=nobita_public_key)
prepared_tx = tx.prepare()

# {
#   "version": 1744830465,
#   "message": null,
#   "fee": 50000,
#   "amount": 1000000,
#   "timeStamp": 97228774,
#   "recipient": "NDADL5VH4WI47UIE3LZGFVWFEBDHF4PL76YQ3EZP",
#   "signer": "984d1f8f6e58b99d62ec30b37d3c3e3aee89dfe74d253009bf11fbd2997b8877",
#   "deadline": 97232374,
#   "type": 257
# }

res = request.send(prepared_tx, nobita_secret_key, endpoint)

```

### Send Mosaic

Case: send Mosaic from **Nobita** to **Suneo**

```python
from nemsdk import request
from nemsdk.tx import TransferTx2
from nemsdk.mosaic import create_attachment

mosaic = create_attachment('dorayaki', 'coin', 1, initial_supply=1000, divisibility=1)

tx = TransferTx2(recipient=suneo_address, signer=nobita_public_key, mosaics=mosaic)
prepared_tx = tx.prepare()

# {
#   "signer": "984d1f8f6e58b99d62ec30b37d3c3e3aee89dfe74d253009bf11fbd2997b8877",
#   "version": 1744830466,
#   "mosaics": [
#     {
#       "quantity": 1,
#       "mosaicId": {
#         "namespaceId": "dorayaki",
#         "name": "coin"
#       }
#     }
#   ],
#   "amount": 1000000,
#   "recipient": "NDADL5VH4WI47UIE3LZGFVWFEBDHF4PL76YQ3EZP",
#   "type": 257,
#   "timeStamp": 97230116,
#   "deadline": 97233716,
#   "message": null,
#   "fee": 150000
# }

res = request.send(prepared_tx, nobita_secret_key, endpoint)
```

### Add Message

```python
from nemsdk.message import Message

message = Message(message='Hello!!', message_type=1)
msg = message.prepare()

# {'type': 1, 'payload': '48656c6c6f2121'}

message = Message(message='Hello!!', message_type=2)
msg = message.prepare(nobita_secret_key, suneo_public_key)

# {'type': 2, 'payload': 'b5a951862efa78123d8....3ca5b0ae54bf08cbc8d6'}

tx = TransferTx1(message=msg)
```

### Multisig Transaction

Just use `prepare_multisig()`

```python
[Doraemon(Multisig Account)]
dora_secret_key = '90cb6d804f5467c9ba64855dd59a88b5eaa033864accf6e3b29d6e6b52e04958'
dora_public_key = 'e5195174aa58a59ca315c2b053b05260c78ea0f8ae4192eb2b31f0c588185f99'
dora_address = 'NBDDMUS6P22IPIMQQ2C42EUHEJISTUUCQ6LV7GLX'

Cosignatories: Nobita, Suneo
```

Case: send xem from **Doraemon** to **Shizuka**(transaction started by **Nobita**)

```python
from nemsdk import request
from nemsdk.tx import TransferTx1


tx = TransferTx1(amount=1, recipient=shizuka_address, signer=dora_public_key)
prepared_tx = tx.prepare_as_multisig(issuer=nobita_public_key)

# {
#   "signer": "984d1f8f6e58b99d62ec30b37d3c3e3aee89dfe74d253009bf11fbd2997b8877",
#   "signatures": [],
#   "timeStamp": 97231430,
#   "type": 4100,
#   "fee": 150000,
#   "deadline": 97235030,
#   "otherTrans": {
#     "signer": "e5195174aa58a59ca315c2b053b05260c78ea0f8ae4192eb2b31f0c588185f99",
#     "timeStamp": 97231430,
#     "type": 257,
#     "fee": 50000,
#     "deadline": 97235030,
#     "amount": 1000000,
#     "message": null,
#     "version": 1744830465,
#     "recipient": "NDSRH5Q5BI7WBWQJCF5NB4KUDKBRW7TVFY2U3ANM"
#   },
#   "version": 1744830465
# }

res = request.send(prepared_tx, nobita_secret_key, endpoint)
# {
#   "message": "SUCCESS",
#   "code": 1,
#   "innerTransactionHash": {
#     "data": "14f34314807886663f62876292be6d780a70942bcbccc03b7ca1515791e4277b"
#   },
#   "transactionHash": {
#     "data": "c02ae75c7362c14445fc31a563a17b5d72bb5823971ed21f78660a18b8038f87"
#   },
#   "type": 1
# }
```

How **Suneo** Sign the above transaction is ...

```python
from nemsdk import request
from nemsdk.tx import MultisigSignatureTx

previous_inner_transaction_hash = '14f34314807886663f62876292be6d780a70942bcbccc03b7ca1515791e4277b'

tx = MultisigSignatureTx(signer=suneo_public_key,
                         target_hash=previous_inner_transaction_hash,
                         target_multisig_address=dora_address)
prepared_tx = tx.prepare()

# {
#   "signer": "a7e78b2eebfffc4cb9ab42790e00ab602df0bf053543c48afd5f19478a877777",
#   "type": 4098,
#   "timeStamp": 97232083,
#   "otherAccount": "NBDDMUS6P22IPIMQQ2C42EUHEJISTUUCQ6LV7GLX",
#   "version": 1744830465,
#   "fee": 150000,
#   "deadline": 97235683,
#   "otherHash": {
#     "data": "14f34314807886663f62876292be6d780a70942bcbccc03b7ca1515791e4277b"
#   }
# }

res = request.send(prepared_tx, suneo_secret_key, endpoint)
```
