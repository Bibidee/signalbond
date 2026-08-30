# Security model

SignalBond hashes exact response bytes before UTF-8 interpretation and fails closed on unavailable, mutable, oversized, or mismatched evidence. Semantic outputs must match the exact JSON schema and validators agree on the derived verdict; rationale and confidence are diagnostics. Challenges require an exact bond and hash-bound counterevidence. Address exclusions are direct address-level restrictions only, not identity or Sybil resistance. DNS resolution and redirect inspection are delegated to GenVM's network sandbox and are a documented platform limitation.
