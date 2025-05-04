from pycardano import (
    Address,
    PoolKeyHash,
    StakeCredential,
    StakeDelegation,
    StakeVerificationKey,
    Transaction,
    TransactionBuilder,
)

from pccontext import ChainContext
from pccontext.exceptions import TransactionError


def stake_delegation(
    context: ChainContext,
    stake_vkey: StakeVerificationKey,
    pool_id: str,
    send_from_addr: Address,
) -> Transaction:
    """
    Generates an unwitnessed stake delegation transaction.
    :param context: The chain context.
    :param stake_vkey: The stake address vkey file.
    :param pool_id: The pool ID (hex) to delegate to.
    :param send_from_addr: The address to send from.
    :return: An unsigned transaction object.
    """
    stake_credential = StakeCredential(stake_vkey.hash())
    stake_delegation_certificate = StakeDelegation(
        stake_credential, PoolKeyHash(bytes.fromhex(pool_id))
    )

    stake_address = Address(staking_part=stake_vkey.hash(), network=context.network)

    stake_address_info = context.stake_address_info(str(stake_address))

    if stake_address_info is not None and len(stake_address_info):
        raise TransactionError(
            f"Stake-Address: {str(stake_address)} is already registered on the chain!\n "
            f"{f"Account is currently delegated to Pool with ID: "
               f" {stake_address_info[0].stake_delegation}\n" if stake_address_info[0].stake_delegation else ''}"
        )

    builder = TransactionBuilder(context)

    builder.add_input_address(send_from_addr)

    builder.certificates = [stake_delegation_certificate]

    transaction_body = builder.build(change_address=send_from_addr)

    return Transaction(transaction_body, builder.build_witness_set())
