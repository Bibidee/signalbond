import hashlib
import json
import pytest
from conftest import warp_to

EVIDENCE_URL = "https://example.com/signal-evidence"
EVIDENCE = b"The signal evidence is stable.\n"
EVIDENCE_HASH = "0x" + hashlib.sha256(EVIDENCE).hexdigest()
COUNTER_URL = "https://example.com/counter-default"
COUNTER = b"Independent counterevidence.\n"
COUNTER_HASH = "0x" + hashlib.sha256(COUNTER).hexdigest()
BENEFICIARY = bytes.fromhex("22" * 20)
BOND = 10**18

def deploy(direct_vm, direct_deploy):
    contract = direct_deploy("contracts/signalbond.py")
    warp_to(direct_vm, "2026-08-30T00:00:00Z")
    return contract

def submit(direct_vm, contract, signal_id="s-1", window=3600, value=10**20):
    direct_vm.value = value
    contract.submit_claim(signal_id, BENEFICIARY, "A verifiable public signal", EVIDENCE_URL, EVIDENCE_HASH, window)
    direct_vm.value = 0

def review_mock(direct_vm, result=None):
    result = result or {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":90,"rationale":"Evidence supports the claim."}
    direct_vm.mock_web(EVIDENCE_URL, {"status": 200, "body": EVIDENCE})
    direct_vm.mock_llm("You independently verify", json.dumps(result))

def open_challenge(direct_vm, c, direct_alice):
    direct_vm.mock_web(COUNTER_URL, {"status": 200, "body": COUNTER})
    direct_vm.mock_llm("COUNTEREVIDENCE_ADMISSION", json.dumps({"relevant_to_claim":"yes","material_to_review":"yes","weakens_or_contradicts":"yes"}))
    direct_vm.value = BOND
    with direct_vm.prank(direct_alice): c.challenge_claim("s-1", COUNTER_URL, COUNTER_HASH, "counter")
    direct_vm.value = 0

def test_submission_and_info(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c)
    s = c.get_signal("s-1")
    assert s["status"] == "pending" and s["escrow_held"] == str(10**20)
    assert s["challenge_window"] == "3600" and int(s["review_deadline"]) > int(s["submitted_at"])
    assert c.get_info()["version"] == "0.3.0"

def test_duplicate_and_invalid_submission_rejected(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c)
    direct_vm.value = 10**20
    with direct_vm.expect_revert("Signal unavailable"): c.submit_claim("s-1", BENEFICIARY, "x", EVIDENCE_URL, EVIDENCE_HASH, 3600)
    with direct_vm.expect_revert("Invalid challenge window"): c.submit_claim("s-2", BENEFICIARY, "x", EVIDENCE_URL, EVIDENCE_HASH, 3599)
    direct_vm.value = 0

def test_initial_verified_review_and_settlement_boundary(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    assert c.get_signal("s-1")["verdict"] == "verified"
    with direct_vm.expect_revert("Challenge window remains open"): c.settle_claim("s-1")
    warp_to(direct_vm, "2026-08-30T01:00:00Z"); c.settle_claim("s-1")
    assert c.get_signal("s-1")["status"] == "settled" and c.get_signal("s-1")["escrow_held"] == "0"
    with direct_vm.expect_revert("Already settled"): c.settle_claim("s-1")

@pytest.mark.parametrize("field,value", [("claim_supported","no"),("contradiction","yes"),("source_quality","no")])
def test_each_disputed_dimension_refunds_submitter_path(direct_vm, direct_deploy, field, value):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); r={"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":90,"rationale":"unsafe"}; r[field]=value
    review_mock(direct_vm, r); c.review_claim("s-1"); assert c.get_signal("s-1")["verdict"] == "disputed"; c.settle_claim("s-1"); s=c.get_signal("s-1"); assert s["status"] == "settled" and s["escrow_held"] == "0" and s["challenge_bond_held"] == "0"

def test_inconclusive_never_approves(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm, {"claim_supported":"unclear","contradiction":"no","source_quality":"yes","confidence":74,"rationale":"unclear"}); c.review_claim("s-1")
    assert c.get_signal("s-1")["verdict"] == "inconclusive"

def test_pending_expiry_refunds_and_blocks_review(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); warp_to(direct_vm, "2026-09-01T00:00:00Z")
    c.expire_pending("s-1"); s=c.get_signal("s-1"); assert s["status"] == "cancelled" and s["escrow_held"] == "0"
    with direct_vm.expect_revert("not reviewable"): c.review_claim("s-1")

@pytest.mark.parametrize("when,allowed", [("2026-08-31T23:59:59Z", False), ("2026-09-01T00:00:00Z", True), ("2026-09-01T00:00:01Z", True)])
def test_pending_expiry_boundaries(direct_vm, direct_deploy, when, allowed):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); warp_to(direct_vm, when)
    if allowed:
        c.expire_pending("s-1"); assert c.get_signal("s-1")["status"] == "cancelled"
    else:
        with direct_vm.expect_revert("Review deadline remains open"): c.expire_pending("s-1")

def test_challenge_timeout_boundary(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    open_challenge(direct_vm, c, direct_alice); warp_to(direct_vm, "2026-08-30T01:59:59Z")
    with direct_vm.expect_revert("deadline remains open"): c.settle_claim("s-1")
    warp_to(direct_vm, "2026-08-30T02:00:00Z"); c.settle_claim("s-1")
    s=c.get_signal("s-1"); assert s["settlement"] == "timeout_refunded" and s["escrow_held"] == "0" and s["challenge_bond_held"] == "0"

def challenged_review(direct_vm, c, direct_alice, result):
    open_challenge(direct_vm, c, direct_alice)
    assert c.get_signal("s-1")["status"] == "challenged"
    with direct_vm.expect_revert("Challenge window remains open"): c.review_claim("s-1")
    direct_vm.clear_mocks(); review_mock(direct_vm, result)
    warp_to(direct_vm, "2026-08-30T01:00:00Z")
    c.review_claim("s-1")

def test_challenged_verified_slashes_bond_and_settles_once(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    challenged_review(direct_vm, c, direct_alice, {"claim_supported":"yes","contradiction":"no","source_quality":"yes","confidence":95,"rationale":"still verified"})
    s=c.get_signal("s-1"); assert s["status"] == "reviewed" and s["verdict"] == "verified"
    assert s["challenge_bond_held"] == "0" and s["escrow_held"] == str(10**20) and s["settlement"] == "slashed"
    with direct_vm.expect_revert("Signal cannot be challenged"): c.challenge_claim("s-1")
    warp_to(direct_vm, "2026-08-30T02:00:00Z"); c.settle_claim("s-1")
    s=c.get_signal("s-1"); assert s["status"] == "settled" and s["escrow_held"] == "0"
    with direct_vm.expect_revert("Already settled"): c.settle_claim("s-1")

@pytest.mark.parametrize("result,settlement", [
    ({"claim_supported":"no","contradiction":"no","source_quality":"yes","confidence":90,"rationale":"disputed"}, "refunded"),
    ({"claim_supported":"unclear","contradiction":"no","source_quality":"yes","confidence":60,"rationale":"unclear"}, "refunded"),
])
def test_challenged_nonverified_reviews_refund_bond_and_principal(direct_vm, direct_deploy, direct_alice, result, settlement):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    challenged_review(direct_vm, c, direct_alice, result)
    s=c.get_signal("s-1"); assert s["status"] == "reviewed" and s["challenge_bond_held"] == "0" and s["settlement"] == settlement
    c.settle_claim("s-1"); s=c.get_signal("s-1"); assert s["status"] == "settled" and s["escrow_held"] == "0" and s["challenge_bond_held"] == "0"
    with direct_vm.expect_revert("Already settled"): c.settle_claim("s-1")

def test_eligible_challenge_and_timeout_refunds_both_balances(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    open_challenge(direct_vm, c, direct_alice); s=c.get_signal("s-1"); assert s["status"] == "challenged" and s["challenge_bond_held"] == str(10**18)
    warp_to(direct_vm, "2026-08-30T02:00:00Z"); c.settle_claim("s-1"); s=c.get_signal("s-1"); assert s["status"] == "settled" and s["escrow_held"] == "0" and s["challenge_bond_held"] == "0"

def test_interested_parties_cannot_challenge(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1"); direct_vm.value=10**18
    with direct_vm.expect_revert("Interested party"): c.challenge_claim("s-1")
    direct_vm.value=0

def test_counterevidence_url_is_in_semantic_prompt(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    counter_url = "https://example.com/counter-evidence"
    counter = b"Counterevidence is stable.\n"
    counter_hash = "0x" + hashlib.sha256(counter).hexdigest()
    direct_vm.mock_web(counter_url, {"status": 200, "body": counter})
    direct_vm.mock_llm("COUNTEREVIDENCE_ADMISSION", json.dumps({"relevant_to_claim":"yes","material_to_review":"yes","weakens_or_contradicts":"yes"}))
    direct_vm.value = 10**18
    with direct_vm.prank(direct_alice): c.challenge_claim("s-1", counter_url, counter_hash, "Counter summary")
    direct_vm.value = 0
    direct_vm.clear_mocks()
    direct_vm.mock_web(EVIDENCE_URL, {"status": 200, "body": EVIDENCE})
    direct_vm.mock_llm(counter_url, json.dumps({"claim_supported":"no","contradiction":"yes","source_quality":"yes","confidence":90,"rationale":"counter"}))
    warp_to(direct_vm, "2026-08-30T01:30:00Z")
    c.review_claim("s-1")
    assert c.get_signal("s-1")["verdict"] == "disputed"

def test_challenge_bond_exact_value_required(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    direct_vm.value = 1
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("Exact challenge bond required"): c.challenge_claim("s-1")
    direct_vm.value = 0

@pytest.mark.parametrize("value", [0, BOND - 1, BOND + 1, BOND * 2])
def test_challenge_bond_rejected_values_are_atomic(direct_vm, direct_deploy, direct_alice, value):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    direct_vm.value = value
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("Exact challenge bond required"): c.challenge_claim("s-1")
    direct_vm.value = 0
    s=c.get_signal("s-1")
    assert s["status"] == "reviewed" and s["verdict"] == "verified" and s["challenge_bond_held"] == "0"
    assert s["challenge_artifact_url"] == "" and s["escrow_held"] == str(10**20)

@pytest.mark.parametrize("sender", ["submitter", "beneficiary", "owner", "sink"])
def test_each_interested_party_is_rejected_without_state_change(direct_vm, direct_deploy, direct_alice, sender):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    sink = bytes.fromhex("00" * 18 + "dead")
    addresses = {"submitter": direct_owner_placeholder(direct_vm), "beneficiary": BENEFICIARY, "owner": direct_owner_placeholder(direct_vm), "sink": sink}
    direct_vm.value = BOND
    with direct_vm.prank(addresses[sender]):
        with direct_vm.expect_revert("Interested party"): c.challenge_claim("s-1")
    direct_vm.value = 0
    s=c.get_signal("s-1"); assert s["status"] == "reviewed" and s["verdict"] == "verified" and s["challenge_bond_held"] == "0"

def direct_owner_placeholder(direct_vm):
    return direct_vm.sender

def test_unrelated_party_challenge_accepts_exact_bond(direct_vm, direct_deploy, direct_alice):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    open_challenge(direct_vm, c, direct_alice)
    assert c.get_signal("s-1")["status"] == "challenged"

@pytest.mark.parametrize("url,artifact_hash,summary,status,body", [
    ("https://example.com/counter", "0x" + "0" * 64, "summary", 200, b"counter"),
    ("https://example.com/counter", "0x" + "1" * 64, "summary", 404, b"counter"),
    ("https://example.com/counter", "0x" + "1" * 64, "summary", 200, b""),
    ("http://example.com/counter", "0x" + "1" * 64, "summary", 200, b"counter"),
    ("https://localhost/counter", "0x" + "1" * 64, "summary", 200, b"counter"),
    ("https://127.0.0.1/counter", "0x" + "1" * 64, "summary", 200, b"counter"),
    ("https://[::1]/counter", "0x" + "1" * 64, "summary", 200, b"counter"),
])
def test_failed_counterevidence_admission_is_atomic(direct_vm, direct_deploy, direct_alice, url, artifact_hash, summary, status, body):
    c = deploy(direct_vm, direct_deploy); submit(direct_vm, c); review_mock(direct_vm); c.review_claim("s-1")
    direct_vm.mock_web(url, {"status": status, "body": body})
    direct_vm.value=BOND
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert(): c.challenge_claim("s-1", url, artifact_hash, summary)
    direct_vm.value=0
    s=c.get_signal("s-1"); assert s["status"] == "reviewed" and s["verdict"] == "verified" and s["challenge_bond_held"] == "0" and s["challenge_artifact_url"] == ""
