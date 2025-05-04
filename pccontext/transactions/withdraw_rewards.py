from pycardano import (
    Address,
    StakeVerificationKey,
    Transaction,
    TransactionBuilder,
    Withdrawals,
)

from pccontext import ChainContext
from pccontext.exceptions import TransactionError


def withdraw_rewards(
    context: ChainContext, stake_vkey: StakeVerificationKey, send_from_addr: Address
) -> Transaction:
    """
    Withdraw rewards from a stake address.
    :param context: The chain context.
    :param stake_vkey: The stake address vkey file.
    :param send_from_addr: The address to send from.
    :return: An unsigned transaction object.
    """
    stake_address = Address(staking_part=stake_vkey.hash(), network=context.network)

    stake_address_info = context.stake_address_info(str(stake_address))

    if stake_address_info is None or len(stake_address_info) == 0:
        raise TransactionError(
            "No rewards found on the stake address, Staking Address may not be on chain."
        )

    rewards_sum = sum(
        reward.reward_account_balance
        for reward in stake_address_info
        if reward.reward_account_balance != 0
    )

    withdrawal = Withdrawals({bytes(stake_address): rewards_sum})

    builder = TransactionBuilder(context)

    builder.add_input_address(send_from_addr)

    # utxos = context.utxos(send_from_addr)
    # for utxo in utxos:
    #     builder.add_input(utxo)

    builder.withdrawals = withdrawal

    builder.required_signers = [
        stake_vkey.hash(),
        send_from_addr.payment_part,
    ]

    transaction_body = builder.build(
        change_address=send_from_addr,
        auto_required_signers=False,
        merge_change=True,
    )

    return Transaction(transaction_body, builder.build_witness_set())
