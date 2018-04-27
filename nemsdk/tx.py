from abc import abstractmethod, ABCMeta
from nemsdk.network import get_version, get_rental_fee_sink
from nemsdk.utils.time import get_current_nem_time
from nemsdk.tx_version import *
from nemsdk.tx_type import *
from nemsdk import fee
from nemsdk.utils.convert import to_micro_xem


class Transaction(metaclass=ABCMeta):
    def __init__(self, network='mainnet', expire_sec=3600):
        self.network = network
        self.expire_sec = expire_sec

    @abstractmethod
    def prepare(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def Type(self):
        raise NotImplementedError

    @property
    def Tx_v(self):
        raise NotImplementedError

    def _prepare_fee(self):
        raise NotImplementedError

    def _prepare_version(self):
        return get_version(self.Tx_v, self.network)

    @staticmethod
    def _prepare_timestamp():
        return get_current_nem_time()

    @staticmethod
    def _prepare_deadline(expire=3600):
        return expire + get_current_nem_time()


class MultisigMixIn:
    def prepare_as_multisig(self, issuer, signatures=None):
        inner_entity = self.prepare()
        entity = {
            'timeStamp': inner_entity['timeStamp'],
            'fee': self._prepare_multisig_fee(),
            'type': MULTISIG,
            'deadline': inner_entity['deadline'],
            'version': get_version(1, self.network),
            'signer': issuer,
            'otherTrans': inner_entity,
            'signatures': signatures or []
        }
        return entity

    @staticmethod
    def _prepare_multisig_fee():
        return to_micro_xem(fee.MULTISIG_TX)


class TransferTx1(Transaction, MultisigMixIn):
    Type = TRANSFER
    Tx_v = ONE

    def __init__(self, amount, recipient, signer, message=None, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount
        self.recipient = recipient
        self.signer = signer

        if message is not None:
            assert type(message) is dict, 'message must be type `dict`'
            assert message.get('type'), 'message must have `type`'
            assert message.get('payload') is not None, 'message must have `payload`'

        self.message = message

    def prepare(self):
        entity = {
            "timeStamp": self._prepare_timestamp(),
            "amount": self._prepare_amount(),
            "fee": self._prepare_fee(),
            "recipient": self.recipient,
            "type": self.Type,
            "deadline": self._prepare_deadline(self.expire_sec),
            "message": self.message,
            "version": self._prepare_version(),
            "signer": self.signer
        }
        return entity

    def _prepare_amount(self):
        return to_micro_xem(self.amount)

    def _prepare_fee(self):
        fee_sum = fee.transfer(self.amount, self.message)
        return to_micro_xem(fee_sum)


class TransferTx2(Transaction, MultisigMixIn):
    Type = TRANSFER
    Tx_v = TWO

    def __init__(self, recipient, signer, mosaics, amount=1, message=None, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount
        self.recipient = recipient
        self.signer = signer
        self.mosaics = mosaics if type(mosaics) is list else [mosaics]

        if message is not None:
            assert type(message) is dict, 'message must be type `dict`'
            assert message.get('type'), 'message must have `type`'
            assert message.get('payload') is not None, 'message must have `payload`'

        self.message = message

    def prepare(self):
        entity = {
            "timeStamp": self._prepare_timestamp(),
            "amount": self._prepare_amount(),
            "fee": self._prepare_fee(),
            "recipient": self.recipient,
            "type": self.Type,
            "deadline": self._prepare_deadline(self.expire_sec),
            "message": self.message,
            "version": self._prepare_version(),
            "signer": self.signer,
            "mosaics": self._prepare_mosaics()
        }
        return entity

    def _prepare_amount(self):
        return to_micro_xem(self.amount)

    def _prepare_fee(self):
        fee_ = fee.transfer(self.amount, self.message, self.mosaics)
        return to_micro_xem(fee_)

    def _prepare_mosaics(self):
        def _extract(mosaic):
            return {k: mosaic[k] for k in ['mosaicId', 'quantity']}

        return [_extract(mosaic)for mosaic in self.mosaics]


class MultisigSignatureTx(Transaction):
    Type = MULTISIG_SIGNATURE
    Tx_v = ONE

    def __init__(self, signer, target_hash, target_multisig_address, **kwargs):
        super().__init__(**kwargs)
        self.signer = signer
        self.other_hash = target_hash
        self.other_account = target_multisig_address

    def prepare(self):
        entity = {
            'timeStamp': self._prepare_timestamp(),
            'fee': self._prepare_fee(),
            'type': self.Type,
            'deadline': self._prepare_deadline(self.expire_sec),
            'version': self._prepare_version(),
            'signer': self.signer,
            'otherHash': {'data': self.other_hash},
            'otherAccount': self.other_account,
        }
        return entity

    def _prepare_fee(self):
        return to_micro_xem(fee.MULTISIG_SIGNATURE_TX)


class MultisigAggregateModificationTx(Transaction, MultisigMixIn):
    Type = MULTISIG_AGGREGATE_MODIFICATION_TRANSFER

    def __init__(self, signer, modifications=None, relative_change=0, **kwargs):
        super().__init__(**kwargs)
        self.signer = signer
        self.relative_change = relative_change

        if modifications:
            assert type(modifications) is list, 'modifications must be type `list`'

        self.modifications = modifications or []

    def prepare(self, *args, **kwargs):
        entity = {
            'timeStamp': self._prepare_timestamp(),
            'fee': self._prepare_fee(),
            'type': self.Type,
            'deadline': self._prepare_deadline(self.expire_sec),
            'version': self._prepare_version(),
            'signer': self.signer,
            'modifications': self.modifications,
        }

        if self._has_relative_change():
            entity['minCosignatories'] = {'relativeChange': self.relative_change}

        return entity

    def add_modification(self, cosignatory_pk, modification_type):
        self.modifications.append({'modificationType': modification_type, 'cosignatoryAccount': cosignatory_pk})

    def modify_relative_change(self, int_value):
        self.relative_change = int_value

    @property
    def Tx_v(self):
        return TWO if self._has_relative_change() else ONE

    def _prepare_fee(self):
        return to_micro_xem(fee.AGGRGATE_MODIFICATION_TX)

    def _has_relative_change(self):
        return self.relative_change != 0


class ProvisionNamespaceTx(Transaction, MultisigMixIn):
    Type = PROVISION_NAMESPACE
    Tx_v = ONE

    def __init__(self, signer, new_part, parent=None, **kwargs):
        super().__init__(**kwargs)
        self.signer = signer
        self.new_part = new_part
        self.parent = parent

    def prepare(self):
        entity = {
            'timeStamp': self._prepare_timestamp(),
            'fee': self._prepare_fee(),
            'type': self.Type,
            'deadline': self._prepare_deadline(self.expire_sec),
            'version': self._prepare_version(),
            'signer': self.signer,
            'newPart': self.new_part,
            'rentalFee': self._prepare_rental_fee(),
            'parent': self.parent,
            'rentalFeeSink': self._prepare_rental_fee_sink()
        }

        return entity

    def _prepare_fee(self):
        return to_micro_xem(fee.PROVISION_NAMESPACE_TX)

    def _prepare_rental_fee(self):
        if self.parent:
            return to_micro_xem(fee.SUB_NAMESPACE_PROVISIONING)
        else:
            return to_micro_xem(fee.ROOT_NAMESPACE_PROVISIONING)

    def _prepare_rental_fee_sink(self):
        return get_rental_fee_sink(self.network)

