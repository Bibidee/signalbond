# State machine

`pending -> reviewed -> settled` is the normal path. Pending review expiry becomes `cancelled`. A verified reviewed signal may enter one challenge round: `reviewed -> challenged -> reviewed` after re-review, or `challenged -> settled` after timeout. Disputed and inconclusive reviews settle to the submitter; verified reviews settle to the beneficiary after the challenge window. Every terminal transition clears escrow and held bond before transfers, preventing replay and double payment.
