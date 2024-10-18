## PyCardano Chain Contexts

This library contains the various Chain Contexts to use with the PyCardano library.

### Basic Usage

#### Blockfrost

```python
from pccontext import BlockFrostChainContext
from blockfrost import ApiUrls

chain_context = BlockFrostChainContext(
    project_id="your_project_id",
    base_url=ApiUrls.mainnet.value
)

```

#### Cardano-CLI

```python
from pccontext import CardanoCliChainContext, CardanoCliNetwork
from pathlib import Path

chain_context = CardanoCliChainContext(
            binary=Path("cardano-cli"),
            socket=Path("node.socket"),
            config_file=Path("config.json"),
            network=CardanoCliNetwork.MAINNET,
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
