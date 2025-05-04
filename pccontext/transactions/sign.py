from typing import List, Tuple

from pycardano import (
    SigningKey,
    Transaction,
    TransactionBody,
    VerificationKey,
    VerificationKeyWitness,
)

from pccontext.transactions.assemble import assemble_transaction


def sign_transaction(
    tx_body: TransactionBody,
    keys: List[Tuple[VerificationKey, SigningKey]],
) -> Transaction:
    """
    Sign the transaction with the provided verification key witnesses.
    :param tx_body: The transaction body to sign.
    :param keys: List of tuples containing verification keys and their corresponding signing keys.
    :return: The signed transaction.
    """
    vkey_witnesses = []
    for verification_key, signing_key in keys:
        vkey_witness = VerificationKeyWitness(
            verification_key, signing_key.sign(tx_body.hash())
        )
        vkey_witnesses.append(vkey_witness)

    return assemble_transaction(
        tx_body=tx_body,
        vkey_witnesses=vkey_witnesses,
    )
