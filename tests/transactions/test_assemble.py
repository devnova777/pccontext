from pycardano import (
    Address,
    PaymentSigningKey,
    PaymentVerificationKey,
    StakeSigningKey,
    StakeVerificationKey,
    VerificationKeyWitness,
)

from pccontext.transactions.assemble import assemble_transaction
from pccontext.transactions.stake_address_registration import stake_address_registration


def test_assemble_transaction(
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

    tx_body = transaction.transaction_body

    vkey_witnesses = [
        VerificationKeyWitness(payment_vkey, payment_skey.sign(tx_body.hash())),
        VerificationKeyWitness(stake_vkey, stake_skey.sign(tx_body.hash())),
    ]

    assembled_tx = assemble_transaction(
        tx_body=tx_body,
        vkey_witnesses=vkey_witnesses,
    )

    assert assembled_tx is not None
    assert assembled_tx.transaction_body == transaction.transaction_body
    assert assembled_tx.valid is True
    assert len(assembled_tx.transaction_witness_set.vkey_witnesses) == 2
