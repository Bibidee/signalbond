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

def test_equivalence_matrix_is_verdict_only(direct_deploy):
    mod = module_for(direct_deploy)
    inconclusive_a = {"claim_supported":"unclear","contradiction":"no","source_quality":"yes","confidence":74,"rationale":"a"}
    inconclusive_b = {"claim_supported":"yes","contradiction":"unclear","source_quality":"unclear","confidence":20,"rationale":"b"}
    disputed = {"claim_supported":"no","contradiction":"no","source_quality":"yes","confidence":99,"rationale":"d"}
    approved = {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":95,"rationale":"safe"}
    assert mod.equivalent(inconclusive_a, inconclusive_b)
    assert not mod.equivalent(disputed, inconclusive_a)
    assert not mod.equivalent(approved, disputed)
    assert mod.equivalent(approved, {**approved, "rationale":"different"})
    assert mod.equivalent(disputed, {**disputed, "contradiction":"yes"})

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

@pytest.mark.parametrize("status,expected", [(404,"bad_http_status"),(408,"http_unavailable"),(425,"http_unavailable"),(429,"http_unavailable"),(500,"http_unavailable")])
def test_http_failure_classes_fail_closed(direct_vm, direct_deploy, status, expected):
    mod = module_for(direct_deploy)
    url = "https://example.com/status"
    body = b"body"
    direct_vm.mock_web(url, {"status": status, "body": body})
    with pytest.raises(ValueError, match=expected):
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

def test_artifact_size_boundaries(direct_vm, direct_deploy):
    mod = module_for(direct_deploy)
    exact = b"a" * mod.MAX_ARTIFACT_BYTES
    url = "https://example.com/size"
    direct_vm.mock_web(url, {"status": 200, "body": exact})
    assert mod.fetch_verified(url, mod.content_hash(exact)) == "a" * mod.MAX_ARTIFACT_BYTES
    too_large = b"a" * (mod.MAX_ARTIFACT_BYTES + 1)
    direct_vm.clear_mocks()
    direct_vm.mock_web(url, {"status": 200, "body": too_large})
    with pytest.raises(ValueError, match="artifact_too_large"): mod.fetch_verified(url, mod.content_hash(too_large))

@pytest.mark.parametrize("field,bad", [("claim_supported","maybe"),("contradiction","YES"),("source_quality",1)])
def test_invalid_enum_values_fail_closed(direct_deploy, field, bad):
    mod = module_for(direct_deploy)
    base = {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":75,"rationale":"ok"}
    base[field] = bad
    assert not mod.valid_analysis(base)

@pytest.mark.parametrize("confidence", [0,74,75,100,-1,101,True,False,"75",75.0,None,[],{}])
def test_confidence_schema_boundaries(direct_deploy, confidence):
    mod = module_for(direct_deploy)
    value = {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":confidence,"rationale":"ok"}
    assert mod.valid_analysis(value) is (isinstance(confidence, int) and not isinstance(confidence, bool) and 0 <= confidence <= 100)

@pytest.mark.parametrize("rationale", ["", "   ", "x" * 401, 0, False, [], {}, None])
def test_rationale_schema_boundaries(direct_deploy, rationale):
    mod = module_for(direct_deploy)
    value = {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":75,"rationale":rationale}
    assert not mod.valid_analysis(value)
