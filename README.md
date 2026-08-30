# SignalBond

SignalBond is a reusable GenLayer Intelligent Contract primitive for escrowed public claims. A submitter commits a statement and the SHA-256 digest of immutable evidence, deposits escrow, and requests independent semantic review. Validators fetch the exact bytes, verify the commitment before interpretation, and compare the deterministic derived verdict rather than rationale text. Verified claims become payable only after the challenge window; disputed or inconclusive claims return escrow to the submitter.

An eligible third party can open one bounded challenge round with the exact required bond and optional hash-bound counterevidence. While challenged, the claim is never actionable. Re-review can slash the bond to the configured sink when verification remains confirmed, or refund it when the result is not verified. If review is unavailable, a public timeout route refunds the bond. All payouts zero internal accounting before transfer and settlement is one-time.

The contract is deliberately frontend- and oracle-independent. External artifacts must be HTTPS, bounded, UTF-8 text and content-addressed by SHA-256(raw bytes). Direct Mode tests cover malformed inputs, integrity failures, consensus disagreement, challenge timing, replay protection, and bond accounting.
