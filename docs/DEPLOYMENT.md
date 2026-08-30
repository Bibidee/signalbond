# Deployment

## CURRENT RELEASE DEPLOYMENT

Final hardened source deployment (v0.3.0): `0xBFd8a850Eb490c9D4aA500b2610BF6ca122d6320` ([Explorer](https://explorer-studio.genlayer.com/address/0xBFd8a850Eb490c9D4aA500b2610BF6ca122d6320)); deployment transaction `0xca7d74bbf9ebc4d50895fc885e8e920d86f52fabbe0598bacfb561305f15fdd2` ([Explorer](https://explorer-studio.genlayer.com/tx/0xca7d74bbf9ebc4d50895fc885e8e920d86f52fabbe0598bacfb561305f15fdd2)). Receipt is FINALIZED with GenVM SUCCESS. Source commit `7882f2f`; local/deployed bytes: 26,303; SHA-256: `c988c078449fcf47c33f358491891df6f9f86b955b853b3ee077787888564b50`; equality: true.

SignalBond v0.3.0 is deployed on StudioNet at `0x0cfAE5Daed6cCF49ECfB8F1b7ebF4cbBf3a569E7` ([Explorer](https://explorer-studio.genlayer.com/address/0x0cfAE5Daed6cCF49ECfB8F1b7ebF4cbBf3a569E7)). Deployment transaction: `0xf1876f5a152d464bd1792274519bd9fe99bf34b65f8bc63b3f18ab7454e1763f` ([Explorer](https://explorer-studio.genlayer.com/tx/0xf1876f5a152d464bd1792274519bd9fe99bf34b65f8bc63b3f18ab7454e1763f)). It finalized with GenVM `SUCCESS`.

The prior v0.2.0 deployment remains historical at `0xc343CEE693AaA8d35493e1D39BA3778CB78138Cc`.

The v0.3.0 deployed source corresponds to contract-source commit `d7e50e2` and SHA-256 `f30202258c3c5354e9a5428b958e1397d72c978c3cdf59494dd277e2cac0e6d7`. `gen_getContractCode` returned 22,217 bytes; local and deployed bytes match exactly.

Direct Mode currently reports 74 passed. Run `python scripts/preflight.py` and `python -m pytest tests/direct -q` from the repository root. Preflight enforces AST parsing, GenVM lint, contract validation/schema, and the complete Direct Mode suite.

## HISTORICAL DEPLOYMENTS

The earlier hardened deployment `0x8Bdf378985B6C11c1D39Fc7306aea568268b5851` and its transaction `0x314a60e8c53e40d24b92df431114cbdc9af7ae9bd9185b9b855ed89deebf5c3b` remain historical. Its source hash was `583df13cb342ceefbbf90c63108d185d3c261f38e67fcaa76549ef21b539fdb5`.

## LIVE EVIDENCE

Finalized evidence includes verified review `0x890cff0b9be0adfc33440720cff8a1c37d63cdc76e45882a6a426aff86d370bf`, inconclusive review `0xb4f4010fb7cffe37c950a88b89d9b217aec6ad75151ae673f2d9d2e329144f2b`, disputed review `0xe4a13122f8eb72aba0b02f522d23b2d3b4475670d98bcdc7c59dc9e44437c503`, and successful disputed settlement `0xaf657ebe49073a58b1127482c61d2b6e251263f583bba979080091c33870f743`. Challenge admission on the historical hardened deployment finalized in transaction `0x0da20e75c0410145cb87bfbe0e9b273741b368590c5b8d437e746e455abfda94`; challenge re-review and timeout remain protocol-time-gated evidence paths.

Latest current-deployment population: verified review `0x384978d08d1e0c7b56845a1150009b391b64655bfde46678d987e82b56ad738e`; disputed review `0x6e0adaaa0c668ad10b09eb2d7a6bfe90db49568fd1ebfa312d63410659bcf621` and settlement `0x35eed0319864c2bee0dfa0414447069e57a2b4d8cacad07ea29941f62a8abba5`; inconclusive review `0x2d7d3c60f38276a681805565b6f173791d2abc779b58a4044db93214e08604a5` and settlement/refund `0xd9d37799ff1bd6ae103a97ddb631ec42cf8720e0f786c6a073c990bd253712cc`. All listed transactions finalized; settlement clears the held escrow. No current-deployment challenge transaction is claimed by this record.

## CI NOTE

The release gate pins the official GenLayer testing-suite commit `8f8e802350140239be2b37590ed7a68253634ec5` (fix #81). This preserves the published `genlayer-test` 0.29.2 API while resolving the current `genvm-runners-all.tar.xz` bundle name, with fallback compatibility for older releases. Direct Mode, lint, and validation all pass locally with this toolchain. Hosted run [33323447134](https://github.com/Bibidee/signalbond/actions/runs/33323447134) completed successfully.
