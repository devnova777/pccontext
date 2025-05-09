## 0.3.4 (2025-05-09)

### Fix

- enhance stake address validation with active and active_epoch checks

## 0.3.3 (2025-05-09)

### Fix

- add active attribute to StakeAddressInfo and update registration check

## 0.3.2 (2025-05-08)

### Fix

- fix access to rewards_state attributes in StakeAddressInfo

## 0.3.1 (2025-05-05)

### Fix

- handle DRep ID processing for VERIFICATION_KEY_HASH with CIP129

## 0.3.0 (2025-05-04)

### Feat

- add transaction assembly and signing functionality

### Fix

- store transaction ID from command execution

## 0.2.12 (2025-04-21)

### Fix

- remove network args from tx id
- handle protocol parameters better

## 0.2.11 (2025-04-03)

### Fix

- add property_from_dict to handle genesis

## 0.2.10 (2025-04-03)

### Fix

- set default era to Conway

## 0.2.9 (2025-04-03)

### Fix

- create genesis params from config files

## 0.2.8 (2025-03-21)

### Fix

- update to latest pycardano

## 0.2.7 (2025-02-04)

### Fix

- add compatibility with Python 3.13

## 0.2.6 (2025-01-10)

### Fix

- convert time to int timestamp

## 0.2.5 (2025-01-10)

### Fix

- save genesis_param

## 0.2.4 (2024-11-26)

### Fix

- use correct Shelley

## 0.2.3 (2024-11-26)

### Fix

- handle transactions with latest cli

## 0.2.2 (2024-11-07)

### Fix

- return instead of raise
- add sort keys
- use PyCardano base models

## 0.2.1 (2024-11-02)

### Fix

- add calculate epoch and tip to OffflineContext

## 0.2.0 (2024-10-24)

### Feat

- added yaci devkit as a backend

### Fix

- improve reference script handling
- add PlutusV3 support
- improve handle various property names
- use Network and Era enum
- add network enum for network name
- add plutusV3 support and protocol_param from wrapped_backend
- add plutusV3 support
- update backends to output PycardanoProtocolParameters
- update models with latest changes
