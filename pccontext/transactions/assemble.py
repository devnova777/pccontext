from typing import Any, List, Optional, Union

from pycardano import (
    NativeScript,
    NonEmptyOrderedSet,
    PlutusV1Script,
    PlutusV2Script,
    PlutusV3Script,
    Redeemers,
    Transaction,
    TransactionWitnessSet,
    VerificationKeyWitness,
)


def assemble_transaction(
    transaction: Transaction,
    vkey_witnesses: Optional[
        Union[List[VerificationKeyWitness], NonEmptyOrderedSet[VerificationKeyWitness]]
    ] = None,
    native_scripts: Optional[
        Union[List[NativeScript], NonEmptyOrderedSet[NativeScript]]
    ] = None,
    bootstrap_witness: Optional[List[Any]] = None,
    plutus_v1_script: Optional[
        Union[List[PlutusV1Script], NonEmptyOrderedSet[PlutusV1Script]]
    ] = None,
    plutus_data: Optional[List[Any]] = None,
    redeemer: Optional[Redeemers] = None,
    plutus_v2_script: Optional[
        Union[List[PlutusV2Script], NonEmptyOrderedSet[PlutusV2Script]]
    ] = None,
    plutus_v3_script: Optional[
        Union[List[PlutusV3Script], NonEmptyOrderedSet[PlutusV3Script]]
    ] = None,
) -> Transaction:
    """
    Assembles a transaction with the provided transaction and witnesses.

    :param transaction: The transaction.
    :param vkey_witnesses: Optional list of verification key witnesses.
    :param native_scripts: Optional list of native scripts.
    :param bootstrap_witness: Optional list of bootstrap witnesses.
    :param plutus_v1_script: Optional list of Plutus V1 scripts.
    :param plutus_data: Optional list of Plutus data.
    :param redeemer: Optional redeemer information.
    :param plutus_v2_script: Optional list of Plutus V2 scripts.
    :param plutus_v3_script: Optional list of Plutus V3 scripts.
    :return: The assembled transaction.
    """
    transaction.transaction_witness_set = TransactionWitnessSet(
        vkey_witnesses=vkey_witnesses,
        native_scripts=native_scripts,
        bootstrap_witness=bootstrap_witness,
        plutus_v1_script=plutus_v1_script,
        plutus_data=plutus_data,
        redeemer=redeemer,
        plutus_v2_script=plutus_v2_script,
        plutus_v3_script=plutus_v3_script,
    )

    return transaction
