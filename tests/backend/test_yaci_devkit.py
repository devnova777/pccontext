from unittest.mock import patch

from pycardano import TransactionInput, TransactionOutput, Address, Value, MultiAsset
from yaci_client.models import EpochNo, ProtocolParamsDto, Utxo

from pccontext import ProtocolParameters


class TestCardanoCliChainContext:
    def test_epoch(self, yaci_devkit_chain_context):
        with patch(
            "yaci_client.api.local_epoch_service.get_latest_epoch.sync",
            return_value=EpochNo(epoch=100),
        ):
            assert yaci_devkit_chain_context.epoch == 100

    def test_protocol_param(self, yaci_devkit_chain_context, yaci_protocol_parameters):
        with patch(
            "yaci_client.api.local_epoch_service.get_latest_protocol_params.sync",
            return_value=ProtocolParamsDto.from_dict(yaci_protocol_parameters),
        ):
            protocol_param = yaci_devkit_chain_context.protocol_param
            expected_protocol_param = ProtocolParameters.from_json(
                yaci_protocol_parameters
            )
            assert protocol_param == expected_protocol_param.to_pycardano()

    def test_utxo(self, yaci_devkit_chain_context, yaci_utxos):
        with patch(
            "yaci_client.api.address_service.get_utxos_1.sync",
            return_value=[Utxo(**utxo) for utxo in yaci_utxos],
        ):
            results = yaci_devkit_chain_context.utxos(
                "addr_test1qraen6hr9zs5yae8cxnhlkh7rk2nfl7rnpg0xvmel3a0xf70v3kz6ee7mtq86x6gmrnw8j7kuf485902akkr7tlcx24qemz34a"
            )

        assert results[0].input == TransactionInput.from_primitive(
            ["a6ce90a9a5ef8ef73858effdae375ba50f302d3c6c8b587a15eaa8fa98ddf741", 0]
        )
        assert results[0].output == TransactionOutput(
            address=Address.from_primitive(
                "addr_test1qraen6hr9zs5yae8cxnhlkh7rk2nfl7rnpg0xvmel3a0xf70v3kz6ee7mtq86x6gmrnw8j7kuf485902akkr7tlcx24qemz34a"
            ),
            amount=Value(coin=10000000000, multi_asset=MultiAsset()),
        )
