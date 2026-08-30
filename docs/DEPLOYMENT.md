# Deployment

Run `python scripts/preflight.py` and `python -m pytest tests/direct -q` from this directory. The deployable source is `contracts/signalbond.py`; record finalized deployment, commit, and SHA-256 of its raw bytes, then retrieve Explorer source and compare byte-for-byte. Run safe, disputed, inconclusive, pending-expiry, challenge, and timeout paths only after deployment finality. No live deployment is claimed by this package yet.
