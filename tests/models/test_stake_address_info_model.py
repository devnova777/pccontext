import pytest
from pccontext.models.stake_address_info_model import StakeAddressInfo


@pytest.mark.parametrize(
    "address, delegation, reward_account_balance",
    [
        (
            "stake1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0",
            "pool1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0",
            1000,
        ),
        (
            "stake1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0",
            "pool1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0",
            0,
        ),
        (
            "stake1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0",
            "pool1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0",
            -1000,
        ),
    ],
    ids=["valid_balance", "zero_balance", "negative_balance"],
)
def test_stake_address_info_happy_path(address, delegation, reward_account_balance):
    # Act
    stake_address_info = StakeAddressInfo(
        address=address,
        stake_delegation=delegation,
        reward_account_balance=reward_account_balance,
    )

    # Assert
    assert stake_address_info.address == address
    assert stake_address_info.stake_delegation == delegation
    assert stake_address_info.reward_account_balance == reward_account_balance


@pytest.mark.parametrize(
    "address, delegation, reward_account_balance",
    [
        ("", "pool1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0", 1000),
        ("stake1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0", "", 1000),
        (
            "stake1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0",
            "pool1u9xlw0k7z0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0q9x0",
            None,
        ),
    ],
    ids=["empty_address", "empty_delegation", "none_balance"],
)
def test_stake_address_info_edge_cases(address, delegation, reward_account_balance):
    # Act
    stake_address_info = StakeAddressInfo(
        address=address,
        stake_delegation=delegation,
        reward_account_balance=reward_account_balance,
    )

    # Assert
    assert stake_address_info.address == address
    assert stake_address_info.stake_delegation == delegation
    assert stake_address_info.reward_account_balance == reward_account_balance
