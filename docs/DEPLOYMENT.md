# Deployment

Run `python scripts/preflight.py` and `python -m pytest tests/direct -q` from this directory. The deployable source is `contracts/signalbond.py`; record finalized deployment, commit, and SHA-256 of its raw bytes, then retrieve Explorer source and compare byte-for-byte. Run safe, disputed, inconclusive, pending-expiry, challenge, and timeout paths only after deployment finality. No live deployment is claimed by this package yet.

Current finalized deployment: `0xF7564AD30F2e1384a9DbC7860e484a15C6B6a96C`; deployment transaction `0x1fd01b31d6a0a2bebb92c29f13f4a888ef62adfee7546a7f0e12c91dc9d2a6e6`; source commit `790c080684697f2226ae5422d89fa19bb4766161`; local source SHA-256 `6a027aaa3c17511d76b4920bc952681e52d784b04c2c2d348b36481a38cc75cd`. The receipt finalized with GenVM `SUCCESS`.

Observed live evidence: submission `0xb5725bcccfd947afcc26e51b15b072cb062c8d18a73f8887bae972ef6bcbfec5`; semantic review `0xb4f4010fb7cffe37c950a88b89d9b217aec6ad75151ae673f2d9d2e329144f2b`, finalized `inconclusive`. Explorer source retrieval/parity and the remaining outcome paths must be recorded separately; no unverified result is presented as approval or dispute.
