## PyCardano Chain Contexts

This library contains the various Chain Contexts to use with the PyCardano library as well as a few 
helper functions for working with and building certain types of transactions.

### Chain Context Usage

#### Blockfrost

```python
from pccontext import BlockFrostChainContext, Network

chain_context = BlockFrostChainContext(
    project_id="your_project_id",
    network=Network.MAINNET,
)

```

#### Cardano-CLI

```python
from pccontext import CardanoCliChainContext, Network
from pathlib import Path

chain_context = CardanoCliChainContext(
            binary=Path("cardano-cli"),
            socket=Path("node.socket"),
            config_file=Path("config.json"),
            network=Network.MAINNET,
)

```

#### Koios

```python
from pccontext import KoiosChainContext

chain_context = KoiosChainContext(api_key="api_key")

```

#### Ogmios

```python
from pccontext import OgmiosChainContext

chain_context = OgmiosChainContext(host="localhost", port=1337)

```

#### Kupo

```python
from pccontext import OgmiosChainContext, KupoChainContextExtension

ogmios_chain_context = OgmiosChainContext(host="localhost", port=1337)
chain_context = KupoChainContextExtension(wrapped_backend=ogmios_chain_context)

```

#### Offline Transfer File

```python
from pathlib import Path
from pccontext import OfflineTransferFileContext

chain_context = OfflineTransferFileContext(offline_transfer_file=Path("offline-transfer.json"))

```

#### Yaci Devkit

```python
from pccontext import YaciDevkitChainContext

chain_context = YaciDevkitChainContext(api_url="http://localhost:8080")

```

### Transactions Usage

```python
from pycardano import (
    Address,
    StakeSigningKey,
    StakeVerificationKey,
    PaymentSigningKey,
    PaymentVerificationKey,
)

from pccontext.transactions import stake_address_registration
import os

from pccontext import BlockFrostChainContext, Network


network = Network.PREPROD
blockfrost_api_key = os.getenv("BLOCKFROST_API_KEY_PREPROD")
chain_context = BlockFrostChainContext(
    project_id=blockfrost_api_key, network=network
)

payment_signing_key = PaymentSigningKey.generate()
payment_verification_key = PaymentVerificationKey.from_signing_key(
    payment_signing_key
)

stake_signing_key = StakeSigningKey.generate()
stake_verification_key = StakeVerificationKey.from_signing_key(stake_signing_key)

address = Address(
    payment_part=payment_verification_key.hash(),
    staking_part=stake_verification_key.hash(),
    network=network.get_network(),
)

# Example Stake Address Registration Transaction
signed_stake_address_registration_tx = stake_address_registration(
    context=chain_context,
    stake_vkey=stake_verification_key,
    send_from_addr=address,
    signing_keys=[payment_signing_key, stake_signing_key],
)

print(f"Signed Transaction: {signed_stake_address_registration_tx}")

chain_context.submit_tx(signed_stake_address_registration_tx)

print(f"Transaction ID: {signed_stake_address_registration_tx.id}")


```