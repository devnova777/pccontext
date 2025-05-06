from typing import Optional

from pycardano import (
    Address,
    DRep,
    DRepKind,
    ScriptHash,
    StakeCredential,
    StakeVerificationKey,
    Transaction,
    TransactionBuilder,
    VerificationKeyHash,
    VoteDelegation,
)

from pccontext import ChainContext


def vote_delegation(
    context: ChainContext,
    stake_vkey: StakeVerificationKey,
    send_from_addr: Address,
    drep_kind: DRepKind,
    drep_id: Optional[str] = None,
) -> Transaction:
    """
    Generates an unwitnessed vote delegation transaction.
    :param context: The chain context.
    :param stake_vkey: The stake address vkey file.
    :param send_from_addr: The address to send from.
    :param drep_kind: The DRep kind.
    :param drep_id: The Delegate Representative ID (hex).
    :return: An unsigned transaction object.
    """
    stake_credential = StakeCredential(stake_vkey.hash())

    if drep_kind in [DRepKind.ALWAYS_ABSTAIN, DRepKind.ALWAYS_NO_CONFIDENCE]:
        drep = DRep(drep_kind)
    elif drep_kind == DRepKind.SCRIPT_HASH and drep_id is not None:
        drep = DRep(drep_kind, ScriptHash(bytes.fromhex(drep_id)))
    elif drep_kind == DRepKind.VERIFICATION_KEY_HASH and drep_id is not None:
        drep_bytes = bytes.fromhex(drep_id)
        if len(drep_bytes) == 29:
            drep_bytes = drep_bytes[1:]
        drep = DRep(drep_kind, VerificationKeyHash(drep_bytes))
    else:
        raise ValueError(
            "DRep ID must be provided for DRepKind SCRIPT_HASH or VERIFICATION_KEY_HASH."
        )

    vote_delegation_certificate = VoteDelegation(stake_credential, drep)

    builder = TransactionBuilder(context)

    builder.add_input_address(send_from_addr)

    builder.certificates = [vote_delegation_certificate]

    transaction_body = builder.build(change_address=send_from_addr)

    return Transaction(transaction_body, builder.build_witness_set())
