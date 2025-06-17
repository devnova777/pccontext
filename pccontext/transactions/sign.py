from typing import List

from pycardano import SigningKey, Transaction, TransactionBody

from pccontext.transactions.assemble import assemble_transaction
from pccontext.transactions.witness import witness


def sign_transaction(
    tx_body: TransactionBody,
    keys: List[SigningKey],
) -> Transaction:
    """
    Sign the transaction with the provided verification key witnesses.
    :param tx_body: The transaction body to sign.
    :param keys: List of signing keys.
    :return: The signed transaction.
    """
    vkey_witnesses = witness(tx_body, keys)

    return assemble_transaction(
        tx_body=tx_body,
        vkey_witnesses=vkey_witnesses,
    )
