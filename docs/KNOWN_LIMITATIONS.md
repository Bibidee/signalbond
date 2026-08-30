# Known limitations

GenVM controls external network reachability; the contract cannot perform reliable DNS resolution or inspect every redirect destination. Evidence must therefore be HTTPS and hash pinned, with sandbox-level network policy providing additional SSRF containment. UTF-8 is intentionally required for semantic interpretation, although hashing always uses the raw bytes. Address-level interested-party exclusions cannot establish real-world identity or prevent Sybil wallets.
