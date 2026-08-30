import hashlib
import sys
import pytest

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

def test_rationale_requires_string_and_transient_errors_group(direct_deploy):
    mod = module_for(direct_deploy)
    base = {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":75,"rationale":"ok"}
    bad = dict(base); bad["rationale"] = {"text":"ok"}
    assert not mod.valid_analysis(bad)
    assert mod.error_equivalent("fetch_unavailable", "http_unavailable")
    assert not mod.error_equivalent("hash_mismatch", "http_unavailable")

def test_private_and_userinfo_urls_rejected(direct_deploy):
    mod = module_for(direct_deploy)
    for value in ("https://127.0.0.1/x", "https://user@127.0.0.1/x", "https://localhost/x", "https://10.0.0.1/x", "https://192.168.1.1/x", "https://172.16.0.1/x", "https://169.254.1.1/x", "https://[::1]/x", "https://[fc00::1]/x", "https://[fd00::1]/x", "https://[fe80::1]/x"):
        try: mod.valid_url(value)
        except Exception: continue
        assert False, value
    assert mod.valid_url("https://example.com/evidence") == "https://example.com/evidence"
    assert mod.valid_url("https://fcdomain.example/x") == "https://fcdomain.example/x"
    assert mod.valid_url("https://fdexample.com/x") == "https://fdexample.com/x"

def test_model_boundaries_and_extra_fields(direct_deploy):
    mod = module_for(direct_deploy)
    base = {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":75,"rationale":"ok"}
    assert mod.verdict(base) == mod.VERIFIED
    assert mod.verdict({**base, "confidence": 74}) == mod.INCONCLUSIVE
    assert mod.verdict({**base, "confidence": 100, "extra": "ignored"}) == mod.VERIFIED
    assert not mod.valid_analysis({**base, "confidence": True})
    assert not mod.valid_analysis({**base, "rationale": ""})
    assert not mod.valid_analysis({**base, "rationale": 4})

@pytest.mark.parametrize("status", [404, 408, 425, 429, 500])
def test_http_failure_classes_fail_closed(direct_vm, direct_deploy, status):
    mod = module_for(direct_deploy)
    url = "https://example.com/status"
    body = b"body"
    direct_vm.mock_web(url, {"status": status, "body": body})
    with pytest.raises(ValueError):
        mod.fetch_verified(url, "0x" + hashlib.sha256(body).hexdigest())

def test_empty_and_invalid_utf8_fail_closed(direct_vm, direct_deploy):
    mod = module_for(direct_deploy)
    empty = "https://example.com/empty"
    direct_vm.mock_web(empty, {"status": 200, "body": b""})
    with pytest.raises(ValueError, match="empty_response"): mod.fetch_verified(empty, "0x" + "0" * 64)
    bad = b"\xff\xfe"
    invalid = "https://example.com/invalid"
    direct_vm.mock_web(invalid, {"status": 200, "body": bad})
    with pytest.raises(ValueError, match="invalid_utf8"): mod.fetch_verified(invalid, "0x" + hashlib.sha256(bad).hexdigest())
