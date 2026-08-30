import sys

def mod(direct_deploy):
    c = direct_deploy("contracts/signalbond.py")
    return sys.modules[c.__class__.__module__]

def a(r, m, w):
    return {"relevant_to_claim": r, "material_to_review": m, "weakens_or_contradicts": w}

def test_admission_decision_matrix(direct_deploy):
    m = mod(direct_deploy)
    assert m.admission_decision(a("yes", "yes", "yes")) == m.ADMIT
    assert m.admission_decision(a("yes", "yes", "unclear")) == m.ADMIT
    for value in (a("yes", "yes", "no"), a("yes", "no", "yes"), a("no", "yes", "yes"), a("no", "no", "no")):
        assert m.admission_decision(value) == m.REJECT

def test_admission_equivalence_compares_decision(direct_deploy):
    m = mod(direct_deploy)
    assert m.admission_equivalent(a("yes", "yes", "yes"), a("yes", "yes", "unclear"))
    assert not m.admission_equivalent(a("yes", "yes", "yes"), a("yes", "yes", "no"))
    assert m.admission_equivalent(a("yes", "no", "yes"), a("no", "yes", "unclear"))

def test_malformed_admission_fails_closed(direct_deploy):
    m = mod(direct_deploy)
    base = a("yes", "yes", "yes")
    for bad in ({"relevant_to_claim":"yes"}, {**base, "extra": "x"}, [], "yes", None, True, {**base, "relevant_to_claim":"YES"}, {**base, "material_to_review":True}, {**base, "weakens_or_contradicts":1}):
        assert m.admission_decision(bad) == m.REJECT
        assert not m.admission_equivalent(base, bad)

def test_policy_hash_matches_canonical_policy(direct_deploy):
    m = mod(direct_deploy)
    assert m.POLICY_HASH == "0x" + m.hashlib.sha256(m.POLICY_CANONICAL.encode("utf-8")).hexdigest()
