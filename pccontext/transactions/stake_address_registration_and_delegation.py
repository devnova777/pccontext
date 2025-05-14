from pycardano import (
    Address,
    PoolKeyHash,
    StakeCredential,
    StakeRegistrationAndDelegation,
    StakeVerificationKey,
    Transaction,
    TransactionBuilder,
)

from pccontext import ChainContext
from pccontext.exceptions import TransactionError


def stake_address_registration_and_delegation(
    context: ChainContext,
    stake_vkey: StakeVerificationKey,
    pool_id: str,
    send_from_addr: Address,
) -> Transaction:
    """
    Generates an unwitnessed stake address registration and delegation transaction.
    :param context: The chain context.
    :param stake_vkey: The stake address vkey file.
    :param pool_id: The pool ID (hex) to delegate to.
    :param send_from_addr: The address to send from.
    :return: An unsigned transaction object.
    """
    protocol_parameters = context.protocol_param

    stake_credential = StakeCredential(stake_vkey.hash())
    registration_and_delegation_certificate = StakeRegistrationAndDelegation(
        stake_credential=stake_credential,
        pool_keyhash=PoolKeyHash(bytes.fromhex(pool_id)),
        coin=protocol_parameters.key_deposit,
    )

    stake_address = Address(staking_part=stake_vkey.hash(), network=context.network)

    stake_address_info = context.stake_address_info(str(stake_address))

    if (
        stake_address_info is not None
        and len(stake_address_info)
        and stake_address_info[0].active
        and stake_address_info[0].active_epoch is not None
    ):
        delegation_pool_id = stake_address_info[0].stake_delegation
        raise TransactionError(
            f"Stake-Address: {str(stake_address)} is already registered on the chain!\n "
            f"{f"Account is currently delegated to Pool with ID: "
               f" {delegation_pool_id}\n" if delegation_pool_id is not None else ''}"
        )

    builder = TransactionBuilder(context)

    builder.add_input_address(send_from_addr)

    builder.certificates = [registration_and_delegation_certificate]

    transaction_body = builder.build(change_address=send_from_addr)

    return Transaction(transaction_body, builder.build_witness_set())
