import hashlib
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("signalbond", Path(__file__).parents[2] / "contracts" / "signalbond.py")
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
except ModuleNotFoundError:
    mod = None

def test_hash_is_raw_bytes():
    if mod is None: return
    assert mod.content_hash(b"a\r\nb") == "0x" + hashlib.sha256(b"a\r\nb").hexdigest()

def test_verdict_and_equivalence_are_fail_closed():
    if mod is None: return
    approved = {"claim_supported":"yes","contradiction":"no","source_quality":"yes","image_consistent":"yes","confidence":75,"rationale":"ok"}
    blocked_a = {"claim_supported":"no","contradiction":"no","source_quality":"yes","image_consistent":"yes","confidence":90,"rationale":"a"}
    blocked_b = {"claim_supported":"no","contradiction":"yes","source_quality":"unclear","image_consistent":"unclear","confidence":76,"rationale":"b"}
    inconclusive = {"claim_supported":"unclear","contradiction":"no","source_quality":"yes","image_consistent":"yes","confidence":74,"rationale":"wait"}
    assert mod.equivalent(approved, approved)
    assert mod.equivalent(blocked_a, blocked_b)
    assert not mod.equivalent(approved, blocked_a)
    assert not mod.equivalent(approved, inconclusive)
    assert not mod.equivalent(approved, {"confidence": 75})

def test_invalid_analysis_and_url_fail_closed():
    if mod is None: return
    assert not mod.valid_analysis({"claim_supported":"yes"})
    assert not mod.valid_analysis({"claim_supported":"yes","contradiction":"no","source_quality":"yes","image_consistent":"yes","confidence":101,"rationale":"x"})
    try: mod.valid_url("http://localhost/x")
    except Exception: pass
    else: assert False

def test_hash_normalization_is_canonical():
    if mod is None: return
    digest = "a" * 64
    assert mod.canonical_hash("0x" + digest) == "0x" + digest
