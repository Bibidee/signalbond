# Deployment

## CURRENT RELEASE DEPLOYMENT

SignalBond v0.2.0 is deployed on StudioNet at `0xc343CEE693AaA8d35493e1D39BA3778CB78138Cc` ([Explorer](https://explorer-studio.genlayer.com/address/0xc343CEE693AaA8d35493e1D39BA3778CB78138Cc)). Deployment transaction: `0xc56ebfe18d89a7b54be8b9129892e997e40066a8a0c2f53162af9bf30215dc6d` ([Explorer](https://explorer-studio.genlayer.com/tx/0xc56ebfe18d89a7b54be8b9129892e997e40066a8a0c2f53162af9bf30215dc6d)). It finalized with GenVM `SUCCESS`.

The deployed source corresponds to contract-source commit `c82900f` and SHA-256 `291ac6438a3dea71778438a4410bdb4942631d660ccada079f69c45088490e0a`. `gen_getContractCode` returned 20,382 bytes; local and deployed bytes match exactly.

Direct Mode currently reports 58 passed. Run `python scripts/preflight.py` and `python -m pytest tests/direct -q` from the repository root. Preflight enforces AST parsing, GenVM lint, contract validation/schema, and the complete Direct Mode suite.

## HISTORICAL DEPLOYMENTS

The earlier hardened deployment `0x8Bdf378985B6C11c1D39Fc7306aea568268b5851` and its transaction `0x314a60e8c53e40d24b92df431114cbdc9af7ae9bd9185b9b855ed89deebf5c3b` remain historical. Its source hash was `583df13cb342ceefbbf90c63108d185d3c261f38e67fcaa76549ef21b539fdb5`.

## LIVE EVIDENCE

Finalized evidence includes verified review `0x890cff0b9be0adfc33440720cff8a1c37d63cdc76e45882a6a426aff86d370bf`, inconclusive review `0xb4f4010fb7cffe37c950a88b89d9b217aec6ad75151ae673f2d9d2e329144f2b`, disputed review `0xe4a13122f8eb72aba0b02f522d23b2d3b4475670d98bcdc7c59dc9e44437c503`, and successful disputed settlement `0xaf657ebe49073a58b1127482c61d2b6e251263f583bba979080091c33870f743`. Challenge admission on the historical hardened deployment finalized in transaction `0x0da20e75c0410145cb87bfbe0e9b273741b368590c5b8d437e746e455abfda94`; challenge re-review and timeout remain protocol-time-gated evidence paths.

## CI NOTE

The release gate pins the official GenLayer testing-suite commit `8f8e802350140239be2b37590ed7a68253634ec5` (fix #81). This preserves the published `genlayer-test` 0.29.2 API while resolving the current `genvm-runners-all.tar.xz` bundle name, with fallback compatibility for older releases. Direct Mode, lint, and validation all pass locally with this toolchain. Hosted run [33322717412](https://github.com/Bibidee/signalbond/actions/runs/33322717412) completed successfully.
