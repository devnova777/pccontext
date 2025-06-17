from typing import List

from pycardano import SigningKey, TransactionBody, VerificationKeyWitness


def witness(
    tx_body: TransactionBody,
    keys: List[SigningKey],
) -> List[VerificationKeyWitness]:
    """
    Witness the transaction with the provided verification and signing keys.
    :param tx_body: The transaction body to sign.
    :param keys: List of signing keys.
    :return: The list of verification key witnesses.
    """
    return [
        VerificationKeyWitness(
            signing_key.to_verification_key(), signing_key.sign(tx_body.hash())
        )
        for signing_key in keys
    ]
