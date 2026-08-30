# ABI reference

Constructor: `owner_address`, `challenge_sink_address`, `challenge_bps`, and `min_challenge_bond`; economics are immutable and bounded.

Writes: `submit_claim(id, beneficiary, statement, evidence_url, evidence_hash, challenge_window)` deposits escrow; `review_claim(id)` performs consensus review; `challenge_claim(id, artifact_url, artifact_hash, summary)` requires exact bond, verified counterevidence, and admission consensus; `expire_pending(id)` refunds expired submissions; `settle_claim(id)` pays the deterministic terminal recipient or timeout refunds.

Views: `get_signal(id)` returns lifecycle, deadlines, escrow/bond accounting, challenger, and diagnostic metadata; `get_info()` returns version, policy, economics, and owner attribution; `get_policy()` returns the immutable policy text/hash.

States are `pending`, `reviewed`, `challenged`, `settled`, and `cancelled`; verdicts are `verified`, `disputed`, and `inconclusive`. Evidence must be HTTPS, bounded UTF-8, and SHA-256(raw bytes) committed. Invalid inputs, unavailable evidence, malformed output, duplicate settlement, and premature timing calls revert or remain retryable without unsafe approval.
