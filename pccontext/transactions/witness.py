from typing import List

from pycardano import SigningKey, Transaction, VerificationKeyWitness


def witness(
    transaction: Transaction,
    keys: List[SigningKey],
) -> List[VerificationKeyWitness]:
    """
    Witness the transaction with the provided verification and signing keys.
    :param transaction: The transaction to sign.
    :param keys: List of signing keys.
    :return: The list of verification key witnesses.
    """
    return [
        VerificationKeyWitness(
            signing_key.to_verification_key(),
            signing_key.sign(transaction.transaction_body.hash()),
        )
        for signing_key in keys
    ]
