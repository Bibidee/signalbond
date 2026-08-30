# Economics

At deployment the challenge rate and minimum bond are immutable. The default is 100 basis points (1%) of escrow, with a minimum of 1 wei-like GEN unit; the rate is bounded to 10%. A challenger must post exactly the stored amount and supply hash-bound counterevidence. A verified re-review slashes the bond to the configured sink; a non-verified re-review or timeout refunds it. Principal always pays the beneficiary only for verified claims and the submitter otherwise.
