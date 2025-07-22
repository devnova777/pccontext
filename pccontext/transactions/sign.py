from typing import List

from pycardano import SigningKey, Transaction

from pccontext.transactions.assemble import assemble_transaction
from pccontext.transactions.witness import witness


def sign_transaction(
    transaction: Transaction,
    keys: List[SigningKey],
) -> Transaction:
    """
    Sign the transaction with the provided verification key witnesses.
    :param transaction: The transaction to sign.
    :param keys: List of signing keys.
    :return: The signed transaction.
    """
    vkey_witnesses = witness(transaction, keys)

    return assemble_transaction(
        transaction=transaction,
        vkey_witnesses=vkey_witnesses,
    )
