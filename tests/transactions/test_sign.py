from pycardano import (
    Address,
    PaymentSigningKey,
    PaymentVerificationKey,
    StakeSigningKey,
    StakeVerificationKey,
)

from pccontext.transactions.sign import sign_transaction
from pccontext.transactions.stake_address_registration import stake_address_registration


def test_sign_transaction(
    chain_context,
):
    """
    Test the assembly of a transaction with various components.
    """
    payment_skey = PaymentSigningKey.generate()
    payment_vkey = PaymentVerificationKey.from_signing_key(payment_skey)
    stake_skey = StakeSigningKey.generate()
    stake_vkey = StakeVerificationKey.from_signing_key(stake_skey)

    address = Address(
        payment_vkey.hash(),
        stake_vkey.hash(),
    )
    transaction = stake_address_registration(chain_context, stake_vkey, address)

    keys = [payment_skey, stake_skey]

    signed_tx = sign_transaction(transaction=transaction, keys=keys)

    assert signed_tx is not None
    assert signed_tx.transaction_body == transaction.transaction_body
    assert signed_tx.valid is True
    assert len(signed_tx.transaction_witness_set.vkey_witnesses) == 2
