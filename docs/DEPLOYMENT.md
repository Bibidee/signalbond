# Deployment

## CURRENT RELEASE DEPLOYMENT

SignalBond v0.3 admission-validity release is deployed at `0x96C19E1D08Acb1Ba3275C82e3783Cd1060Af88Bf` ([Explorer](https://explorer-studio.genlayer.com/address/0x96C19E1D08Acb1Ba3275C82e3783Cd1060Af88Bf)). Deployment transaction: `0x188c2680480ed692861d9183c3d642b010429ebd7d5f0758ba2bc7491a46f72b` ([Explorer](https://explorer-studio.genlayer.com/tx/0x188c2680480ed692861d9183c3d642b010429ebd7d5f0758ba2bc7491a46f72b)). Finalized with GenVM SUCCESS. Source commit `bceb3a3`; local/deployed bytes 26,953; SHA-256 `54f20e9880474796ee211df1e39068fbbeb2f2e34897d4375f27b51efd1f8aeb`; parity exact.

The prior `0xBCC15C4...` deployment is historical.

Direct Mode currently reports 79 passed. Run `python scripts/preflight.py` and `python -m pytest tests/direct -q` from the repository root. Preflight enforces AST parsing, GenVM lint, contract validation/schema, and the complete Direct Mode suite.

## HISTORICAL DEPLOYMENTS

The previous v0.3 deployment `0xBFd8a850Eb490c9D4aA500b2610BF6ca122d6320` and transaction `0xca7d74bbf9ebc4d50895fc885e8e920d86f52fabbe0598bacfb561305f15fdd2` remain historical (source commit `7882f2f`, SHA-256 `c988c078449fcf47c33f358491891df6f9f86b955b853b3ee077787888564b50`). The earlier v0.3 deployment `0x0cfAE5Daed6cCF49ECfB8F1b7ebF4cbBf3a569E7` and transaction `0xf1876f5a152d464bd1792274519bd9fe99bf34b65f8bc63b3f18ab7454e1763f` are also historical. The v0.2 deployment is `0xc343CEE693AaA8d35493e1D39BA3778CB78138Cc`; earlier records include `0xF7564AD30F2e1384a9DbC7860e484a15C6B6a96C` and `0x8Bdf378985B6C11c1D39Fc7306aea568268b5851`.

The earlier hardened deployment `0x8Bdf378985B6C11c1D39Fc7306aea568268b5851` and its transaction `0x314a60e8c53e40d24b92df431114cbdc9af7ae9bd9185b9b855ed89deebf5c3b` remain historical. Its source hash was `583df13cb342ceefbbf90c63108d185d3c261f38e67fcaa76549ef21b539fdb5`.

## CURRENT LIVE CHALLENGE EVIDENCE

Signal `live-challenge-final-001` on `0x96C19E1D08Acb1Ba3275C82e3783Cd1060Af88Bf`: submit `0xd328310efc6ba81290a8a56621df3d6e00d0331692785ada11c178780cf8d9d8`, verified review `0x6976c7a812829abb7139e614fad8deecdc0166544c7d9ef00a4524b1649e609c`, successful challenge `0xd732f4fde0e70ae0c231f8e3954c0ea5ceb43c6f9461e89e2c444b00ee8ad327`. Final state `challenged`; bond required/held `0.01 GEN`; escrow held `1 GEN`; opening ends `2026-08-30T22:54:14Z`; re-review deadline `2026-08-30T23:54:14Z`.

## HISTORICAL LIVE EVIDENCE

Fresh final-deployment claim `live-challenge-final-001`: submit `0xd328310efc6ba81290a8a56621df3d6e00d0331692785ada11c178780cf8d9d8`, verified review `0x6976c7a812829abb7139e614fad8deecdc0166544c7d9ef00a4524b1649e609c`, challenge `0xd732f4fde0e70ae0c231f8e3954c0ea5ceb43c6f9461e89e2c444b00ee8ad327`. All finalized with GenVM SUCCESS; state is `challenged`, bond required/held `10000000000000000`, escrow held `1000000000000000000`. Opening ends `2026-08-30T22:54:14Z`; re-review deadline `2026-08-30T23:54:14Z`.

Final v0.3.0 deployment live evidence: verified review `0x68ed004f9fbf6815ef7320028db84240d4c823a5116ae36bbc47db2318492ea9`; disputed review `0x69cb2482a9af7429900cf3a545309f2f41d86ca2acebc8c0c64f52e01def6ae7` and settlement `0x490b6702f479d524f64a3cc8640688e811d3a5d0b0cc99070e8b6a713c744e29`; inconclusive review `0x9ca2a99eb83b11fa3ea8c9a077ae457441b5f3395383ff332e91673cc703be15` and settlement `0x8fe7731beaf5586ce8cb7673310ae6a48b9c569854ddcd233b5d3225c6315d0a`. All finalized with GenVM SUCCESS; disputed and inconclusive settlements refunded the submitter. Challenge/re-review remains a separate time-gated path.

Canonical challenge attempt `0x2823d6326556ddde0fb4fca9b630525c848df6fca8992c2c7f9eb6f3dc0b54c0` finalized with `[EXPECTED] Signal cannot be challenged`. The call included a real counterevidence URL, SHA-256 hash, and summary, but reverted at the initial eligibility guard before counterevidence validation or nondeterministic relevance admission. No challenge state was created and no bond was retained. Verified settlement `0xe7288ea04164861309b337cb2d6538ffba5510eefb5f14e978069026a295935f` finalized with GenVM SUCCESS and transferred the 1 GEN principal to the beneficiary. Exact challenge-window expiry is not asserted without timestamp verification.

Finalized evidence includes verified review `0x890cff0b9be0adfc33440720cff8a1c37d63cdc76e45882a6a426aff86d370bf`, inconclusive review `0xb4f4010fb7cffe37c950a88b89d9b217aec6ad75151ae673f2d9d2e329144f2b`, disputed review `0xe4a13122f8eb72aba0b02f522d23b2d3b4475670d98bcdc7c59dc9e44437c503`, and successful disputed settlement `0xaf657ebe49073a58b1127482c61d2b6e251263f583bba979080091c33870f743`. Challenge admission on the historical hardened deployment finalized in transaction `0x0da20e75c0410145cb87bfbe0e9b273741b368590c5b8d437e746e455abfda94`; challenge re-review and timeout remain protocol-time-gated evidence paths.

Latest current-deployment population: verified review `0x384978d08d1e0c7b56845a1150009b391b64655bfde46678d987e82b56ad738e`; disputed review `0x6e0adaaa0c668ad10b09eb2d7a6bfe90db49568fd1ebfa312d63410659bcf621` and settlement `0x35eed0319864c2bee0dfa0414447069e57a2b4d8cacad07ea29941f62a8abba5`; inconclusive review `0x2d7d3c60f38276a681805565b6f173791d2abc779b58a4044db93214e08604a5` and settlement/refund `0xd9d37799ff1bd6ae103a97ddb631ec42cf8720e0f786c6a073c990bd253712cc`. All listed transactions finalized; settlement clears the held escrow. No current-deployment challenge transaction is claimed by this record.

## HISTORICAL LIVE EVIDENCE

The older verdict population below belongs to superseded deployments and is historical only.

## CI NOTE

The release gate pins the official GenLayer testing-suite commit `8f8e802350140239be2b37590ed7a68253634ec5` (fix #81). Direct Mode (79 passed), lint, validation/schema, and preflight pass. Hosted run [33337988307](https://github.com/Bibidee/signalbond/actions/runs/33337988307) completed successfully for exact head `2c538b2`.
