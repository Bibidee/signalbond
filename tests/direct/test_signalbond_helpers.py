import hashlib
import sys

def module_for(direct_deploy):
    contract = direct_deploy("contracts/signalbond.py")
    return sys.modules[contract.__class__.__module__]

def test_hash_is_raw_bytes(direct_deploy):
    mod = module_for(direct_deploy)
    assert mod.content_hash(b"a\r\nb") == "0x" + hashlib.sha256(b"a\r\nb").hexdigest()

def test_verdict_and_equivalence_are_fail_closed(direct_deploy):
    mod = module_for(direct_deploy)
    approved = {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":75,"rationale":"ok"}
    blocked_a = {"claim_supported":"no","contradiction":"no","source_quality":"yes","confidence":90,"rationale":"a"}
    blocked_b = {"claim_supported":"no","contradiction":"yes","source_quality":"unclear","confidence":76,"rationale":"b"}
    inconclusive = {"claim_supported":"unclear","contradiction":"no","source_quality":"yes","confidence":74,"rationale":"wait"}
    assert mod.equivalent(approved, approved)
    assert mod.equivalent(blocked_a, blocked_b)
    assert not mod.equivalent(approved, blocked_a)
    assert not mod.equivalent(approved, inconclusive)
    assert not mod.equivalent(approved, {"confidence": 75})

def test_invalid_analysis_and_url_fail_closed(direct_deploy):
    mod = module_for(direct_deploy)
    assert not mod.valid_analysis({"claim_supported":"yes"})
    assert not mod.valid_analysis({"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":101,"rationale":"x"})
    try:
        mod.valid_url("http://localhost/x")
    except Exception:
        pass
    else:
        assert False

def test_hash_normalization_is_canonical(direct_deploy):
    mod = module_for(direct_deploy)
    digest = "a" * 64
    assert mod.canonical_hash("0x" + digest) == "0x" + digest
