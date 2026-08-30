# Design

Lifecycle: `pending -> reviewed(verified|disputed|inconclusive) -> settled`; a verified claim may enter `challenged` during its window. A challenge closes actionability, requires re-review after the opening window, and has a finite review deadline. Successful verified re-review slashes the bond to `challenge_sink`; any other finalized result refunds the challenger. Deadline settlement refunds the bond and leaves the claim inconclusive. No path pays twice.

Consensus is nondeterministic only for independent web observation and semantic interpretation. Hash checks, verdict derivation, authorization, timing, and accounting are deterministic. `equivalent()` compares the derived verdict; diagnostic dimensions and rationale are explanatory only. Approval remains strict: positive support/source/image fields, no contradiction, and confidence at least 75.

Evidence is SHA-256 of exact raw HTTP bytes before UTF-8 decoding. Hash mismatch, unavailable/empty/non-2xx/oversized/invalid UTF-8 content, malformed model output, and consensus disagreement fail closed. One lifetime challenge round keeps storage bounded.
