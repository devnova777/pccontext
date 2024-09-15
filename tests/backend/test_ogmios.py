from fractions import Fraction
from unittest.mock import patch

import pytest
from ogmios.datatypes import (
    ProtocolParameters as OgmiosProtocolParameters,
    EraSummary,
    Era,
)
from pycardano.network import Network
from pycardano.transaction import MultiAsset, TransactionInput
from ogmios.utils import GenesisParameters as OgmiosGenesisParameters

from pccontext.backend import OgmiosChainContext
from pccontext.backend.ogmios import ALONZO_COINS_PER_UTXO_WORD
from pccontext.models import GenesisParameters

PROTOCOL_RESULT = {
    "minFeeCoefficient": 44,
    "minFeeConstant": 155381,
    "maxBlockBodySize": 65536,
    "maxBlockHeaderSize": 1100,
    "maxTxSize": 16384,
    "stakeKeyDeposit": 0,
    "poolDeposit": 0,
    "poolRetirementEpochBound": 18,
    "desiredNumberOfPools": 100,
    "poolInfluence": "0/1",
    "monetaryExpansion": "1/10",
    "treasuryExpansion": "1/10",
    "decentralizationParameter": "1/1",
    "extraEntropy": "neutral",
    "protocolVersion": {"major": 5, "minor": 0},
    "minPoolCost": 0,
    "coinsPerUtxoWord": 1,
    "coinsPerUtxoByte": 1,
    "prices": {"memory": "1/10", "steps": "1/10"},
    "maxExecutionUnitsPerTransaction": {"memory": 500000000000, "steps": 500000000000},
    "maxExecutionUnitsPerBlock": {"memory": 500000000000, "steps": 500000000000},
    "maxValueSize": 4000,
    "collateralPercentage": 1,
    "maxCollateralInputs": 5,
}

GENESIS_RESULT = {
    "systemStart": "2021-12-21T03:17:14.803874404Z",
    "networkMagic": 42,
    "network": "testnet",
    "activeSlotsCoefficient": "1/10",
    "securityParameter": 1000000000,
    "epochLength": 500,
    "slotsPerKesPeriod": 129600,
    "maxKesEvolutions": 60000000,
    "slotLength": 1,
    "updateQuorum": 2,
    "maxLovelaceSupply": 1000000000000,
    "protocolParameters": {
        "minUtxoValue": 1000000,
    },
}

UTXOS = [
    [
        {
            "txId": "3a42f652bd8dee788577e8c39b6217db3df659c33b10a2814c20fb66089ca167",
            "index": 1,
        },
        {
            "address": "addr_test1qraen6hr9zs5yae8cxnhlkh7rk2nfl7rnpg0xvmel3a0xf70v3kz6ee7mtq86x6gmrnw8j7kuf485902akkr7tlcx24qemz34a",
            "value": {"coins": 764295183, "assets": {}},
            "datum": None,
        },
    ],
    [
        {
            "txId": "c93d5dac64e3267abd2a91b9759e0d08395090d7bd89dfdfecd7ccc566661bcd",
            "index": 1,
        },
        {
            "address": "addr_test1qraen6hr9zs5yae8cxnhlkh7rk2nfl7rnpg0xvmel3a0xf70v3kz6ee7mtq86x6gmrnw8j7kuf485902akkr7tlcx24qemz34a",
            "value": {
                "coins": 3241308,
                "assets": {
                    "126b8676446c84a5cd6e3259223b16a2314c5676b88ae1c1f8579a8f.744d494e": 762462,
                    "57fca08abbaddee36da742a839f7d83a7e1d2419f1507fcbf3916522.43484f43": 9945000,
                    "fc3ef8db4a16c1959fbabfcbc3fb7669bf315967ffef260ececc47a3.53484942": 1419813131821,
                    "fc3ef8db4a16c1959fbabfcbc3fb7669bf315967ffef260ececc47a3": 1234,
                },
            },
            "datum": None,
        },
    ],
]


def override_request(method, args):
    if args["query"] == "currentProtocolParameters":
        return PROTOCOL_RESULT
    elif args["query"] == "genesisConfig":
        return GENESIS_RESULT
    elif "utxo" in args["query"]:
        query = args["query"]["utxo"][0]
        if isinstance(query, dict):
            for utxo in UTXOS:
                if (
                    utxo[0]["txId"] == query["txId"]
                    and utxo[0]["index"] == query["index"]
                ):
                    return [utxo]
            return []
        else:
            return UTXOS
    elif "chainTip" in args["query"]:
        return {"slot": 100000000}
    else:
        return None


@pytest.fixture
def chain_context(client):
    with patch(
        "pccontext.backend.ogmios.OgmiosChainContext",
        side_effect=override_request,
    ):
        context = OgmiosChainContext(host="", network=Network.TESTNET)
        # context._request = override_request
    return context


class TestOgmiosChainContext:
    def test_protocol_param(self, ogmios_chain_context, ogmios_protocol_parameters):
        with patch(
            "ogmios.statequery.QueryProtocolParameters.execute",
            return_value=(OgmiosProtocolParameters(**ogmios_protocol_parameters), None),
        ), patch("ogmios.client.connect"):
            protocol_param = ogmios_chain_context.protocol_param

            assert (
                protocol_param.collateral_percent
                == ogmios_protocol_parameters["collateralPercentage"]
            )
            assert (
                protocol_param.committee_max_term_length
                == ogmios_protocol_parameters["constitutionalCommitteeMaxTermLength"]
            )
            assert (
                protocol_param.committee_min_size
                == ogmios_protocol_parameters["constitutionalCommitteeMinSize"]
            )
            assert protocol_param.cost_models == {
                "PlutusV1": ogmios_protocol_parameters["plutusCostModels"]["plutus:v1"],
                "PlutusV2": ogmios_protocol_parameters["plutusCostModels"]["plutus:v2"],
                "PlutusV3": ogmios_protocol_parameters["plutusCostModels"]["plutus:v3"],
            }
            assert (
                protocol_param.d_rep_activity
                == ogmios_protocol_parameters["delegateRepresentativeMaxIdleTime"]
            )
            assert (
                protocol_param.d_rep_deposit
                == ogmios_protocol_parameters["delegateRepresentativeDeposit"]["ada"][
                    "lovelace"
                ]
            )

            assert protocol_param.dvt_motion_no_confidence == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["noConfidence"]
                )
            )

            assert protocol_param.dvt_committee_normal == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["constitutionalCommittee"]["default"]
                )
            )
            assert protocol_param.dvt_committee_no_confidence == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["constitutionalCommittee"]["stateOfNoConfidence"]
                )
            )
            assert protocol_param.dvt_update_to_constitution == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["constitution"]
                )
            )
            assert protocol_param.dvt_hard_fork_initiation == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["hardForkInitiation"]
                )
            )
            assert protocol_param.dvt_p_p_network_group == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["protocolParametersUpdate"]["network"]
                )
            )
            assert protocol_param.dvt_p_p_economic_group == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["protocolParametersUpdate"]["economic"]
                )
            )
            assert protocol_param.dvt_p_p_technical_group == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["protocolParametersUpdate"]["technical"]
                )
            )
            assert protocol_param.dvt_p_p_gov_group == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["protocolParametersUpdate"]["governance"]
                )
            )
            assert protocol_param.dvt_treasury_withdrawal == float(
                Fraction(
                    ogmios_protocol_parameters[
                        "delegateRepresentativeVotingThresholds"
                    ]["treasuryWithdrawals"]
                )
            )
            assert protocol_param.price_mem == float(
                Fraction(ogmios_protocol_parameters["scriptExecutionPrices"]["memory"])
            )
            assert protocol_param.price_step == float(
                Fraction(ogmios_protocol_parameters["scriptExecutionPrices"]["cpu"])
            )
            assert protocol_param.gov_action_deposit == float(
                Fraction(
                    ogmios_protocol_parameters["governanceActionDeposit"]["ada"][
                        "lovelace"
                    ]
                )
            )
            assert protocol_param.gov_action_lifetime == float(
                Fraction(ogmios_protocol_parameters["governanceActionLifetime"])
            )
            assert protocol_param.max_block_size == float(
                ogmios_protocol_parameters["maxBlockBodySize"]["bytes"]
            )
            assert protocol_param.max_block_header_size == float(
                ogmios_protocol_parameters["maxBlockHeaderSize"]["bytes"]
            )
            assert protocol_param.max_tx_size == float(
                ogmios_protocol_parameters["maxTransactionSize"]["bytes"]
            )
            assert protocol_param.max_tx_ex_mem == float(
                ogmios_protocol_parameters["maxExecutionUnitsPerTransaction"]["memory"]
            )
            assert protocol_param.max_tx_ex_steps == float(
                ogmios_protocol_parameters["maxExecutionUnitsPerTransaction"]["cpu"]
            )
            assert protocol_param.max_block_ex_mem == float(
                ogmios_protocol_parameters["maxExecutionUnitsPerBlock"]["memory"]
            )
            assert protocol_param.max_block_ex_steps == float(
                ogmios_protocol_parameters["maxExecutionUnitsPerBlock"]["cpu"]
            )
            assert protocol_param.max_collateral_inputs == float(
                ogmios_protocol_parameters["maxCollateralInputs"]
            )
            assert (
                protocol_param.max_val_size
                == ogmios_protocol_parameters["maxValueSize"]["bytes"]
            )

            assert protocol_param.min_fee_constant == float(
                ogmios_protocol_parameters["minFeeConstant"]["ada"]["lovelace"]
            )
            assert (
                protocol_param.min_fee_coefficient
                == ogmios_protocol_parameters["minFeeCoefficient"]
            )
            assert protocol_param.min_pool_cost == float(
                ogmios_protocol_parameters["minStakePoolCost"]["ada"]["lovelace"]
            )
            assert (
                protocol_param.min_fee_ref_script_cost_per_byte
                == ogmios_protocol_parameters["minFeeReferenceScripts"]
            )
            assert protocol_param.key_deposit == float(
                ogmios_protocol_parameters["stakeCredentialDeposit"]["ada"]["lovelace"]
            )
            assert protocol_param.pool_deposit == float(
                ogmios_protocol_parameters["stakePoolDeposit"]["ada"]["lovelace"]
            )
            assert protocol_param.pool_influence == float(
                Fraction(ogmios_protocol_parameters["stakePoolPledgeInfluence"])
            )
            assert protocol_param.monetary_expansion == float(
                Fraction(ogmios_protocol_parameters["monetaryExpansion"])
            )
            assert protocol_param.treasury_expansion == float(
                Fraction(ogmios_protocol_parameters["treasuryExpansion"])
            )
            assert protocol_param.protocol_major_version == float(
                Fraction(ogmios_protocol_parameters["version"]["major"])
            )
            assert protocol_param.protocol_minor_version == float(
                Fraction(ogmios_protocol_parameters["version"]["minor"])
            )
            assert protocol_param.coins_per_utxo_word == ALONZO_COINS_PER_UTXO_WORD
            assert (
                protocol_param.coins_per_utxo_byte
                == ogmios_protocol_parameters["minUtxoDepositCoefficient"]
            )

    def test_genesis(
        self, ogmios_chain_context, ogmios_era_summary, ogmios_genesis_config
    ):
        with patch(
            "ogmios.statequery.QueryGenesisConfiguration.execute",
            return_value=(ogmios_genesis_config, None),
        ), patch(
            "ogmios.statequery.QueryEraSummaries.execute",
            return_value=(
                ogmios_era_summary,
                None,
            ),
        ), patch(
            "ogmios.client.connect"
        ):
            genesis_param = ogmios_chain_context.genesis_param

        assert genesis_param.active_slots_coefficient == Fraction("1/10")
        assert (
            GenesisParameters(
                active_slots_coefficient=Fraction("1/10"),
                update_quorum=2,
                max_lovelace_supply=1000000000000,
                network_magic=42,
                epoch_length=500,
                system_start=1640056634,
                slots_per_kes_period=129600,
                slot_length=1,
                max_kes_evolutions=60000000,
                security_param=1000000000,
            )
            == chain_context.genesis_param
        )

    def test_utxo(self, chain_context):
        results = chain_context.utxos(
            "addr_test1qraen6hr9zs5yae8cxnhlkh7rk2nfl7rnpg0xvmel3a0xf70v3kz6ee7mtq86x6gmrnw8j7kuf485902akkr7tlcx24qemz34a"
        )

        assert results[0].input == TransactionInput.from_primitive(
            ["3a42f652bd8dee788577e8c39b6217db3df659c33b10a2814c20fb66089ca167", 1]
        )
        assert results[0].output.amount == 764295183

        assert results[1].input == TransactionInput.from_primitive(
            ["c93d5dac64e3267abd2a91b9759e0d08395090d7bd89dfdfecd7ccc566661bcd", 1]
        )
        assert results[1].output.amount.coin == 3241308
        assert results[1].output.amount.multi_asset == MultiAsset.from_primitive(
            {
                "126b8676446c84a5cd6e3259223b16a2314c5676b88ae1c1f8579a8f": {
                    "744d494e": 762462
                },
                "57fca08abbaddee36da742a839f7d83a7e1d2419f1507fcbf3916522": {
                    "43484f43": 9945000
                },
                "fc3ef8db4a16c1959fbabfcbc3fb7669bf315967ffef260ececc47a3": {
                    "53484942": 1419813131821,
                    b"": 1234,
                },
            }
        )

    def test_utxo_by_tx_id(self, chain_context):
        utxo = chain_context.utxo_by_tx_id(
            "3a42f652bd8dee788577e8c39b6217db3df659c33b10a2814c20fb66089ca167",
            1,
        )
        assert utxo.input == TransactionInput.from_primitive(
            ["3a42f652bd8dee788577e8c39b6217db3df659c33b10a2814c20fb66089ca167", 1]
        )
        assert utxo.output.amount == 764295183

        not_utxo = chain_context.utxo_by_tx_id(
            "3a42f652bd8dee788577e8c39b6217db3df659c33b10a2814c20fb66089ca167",
            2,
        )
        assert not_utxo is None
