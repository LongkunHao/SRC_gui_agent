#!/usr/bin/env python3
"""
Sanity check for the Elation Prescriptions app.
Validates that seed data loads correctly and state operations work.
"""

import json
import subprocess
import sys
import time
import requests
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent


def get_seed_state():
    """Load seed data by evaluating data.js via Node."""
    data_js = APP_DIR / "js" / "data.js"
    node_script = """
    const fs = require('fs');
    const code = fs.readFileSync('%s', 'utf8');
    const fn = new Function(code + `; return {
        SEED_DATA_VERSION, CURRENT_USER, CURRENT_PATIENT,
        PERMANENT_RX_MEDS, PERMANENT_OTC_MEDS, TEMPORARY_MEDS,
        DISCONTINUED_MEDS, CANCELED_SCRIPTS, PHARMACIES,
        REFILL_REQUESTS, CHANGE_REQUESTS, RX_TEMPLATES,
        CUSTOM_SIGS, MEDICATION_DATABASE, DRUG_INTERACTIONS,
        FORMULARY_DATA, SETTINGS, PROVIDERS, DIAGNOSIS_CODES,
        UNIT_OPTIONS, FREQUENCY_OPTIONS, DISCONTINUE_REASONS
    }`);
    const data = fn();
    // Build state as the browser would
    const state = {
        _seedVersion: data.SEED_DATA_VERSION,
        currentUser: data.CURRENT_USER,
        currentPatient: data.CURRENT_PATIENT,
        permanentRxMeds: data.PERMANENT_RX_MEDS,
        permanentOtcMeds: data.PERMANENT_OTC_MEDS,
        temporaryMeds: data.TEMPORARY_MEDS,
        discontinuedMeds: data.DISCONTINUED_MEDS,
        canceledScripts: data.CANCELED_SCRIPTS,
        pharmacies: data.PHARMACIES,
        refillRequests: data.REFILL_REQUESTS,
        changeRequests: data.CHANGE_REQUESTS,
        rxTemplates: data.RX_TEMPLATES,
        customSigs: data.CUSTOM_SIGS,
        medicationDatabase: data.MEDICATION_DATABASE,
        drugInteractions: data.DRUG_INTERACTIONS,
        formularyData: data.FORMULARY_DATA,
        settings: data.SETTINGS,
        providers: data.PROVIDERS,
        diagnosisCodes: data.DIAGNOSIS_CODES,
        _nextPrxId: 100,
        _nextOtcId: 100,
        _nextTmpId: 100,
        _nextDiscId: 100,
        _nextCxlId: 100,
        _nextRrId: 100,
        _nextCrId: 100,
        _nextTplId: 100,
        _nextSigId: 100,
        _nextAlgId: 100
    };
    console.log(JSON.stringify(state));
    """ % str(data_js).replace("\\", "\\\\")

    result = subprocess.run(
        ["node", "-e", node_script],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        raise RuntimeError(f"Node.js error: {result.stderr}")
    return json.loads(result.stdout)


def validate_seed_data(state):
    """Validate seed data structure and content."""
    errors = []

    # Check required top-level keys
    required_keys = [
        "currentUser", "currentPatient", "permanentRxMeds", "permanentOtcMeds",
        "temporaryMeds", "discontinuedMeds", "canceledScripts", "pharmacies",
        "refillRequests", "changeRequests", "rxTemplates", "customSigs",
        "medicationDatabase", "drugInteractions", "formularyData", "settings",
        "providers", "diagnosisCodes"
    ]
    for key in required_keys:
        if key not in state:
            errors.append(f"Missing key: {key}")

    # Validate counts
    if len(state.get("permanentRxMeds", [])) < 5:
        errors.append(f"Too few permanent Rx meds: {len(state.get('permanentRxMeds', []))}")
    if len(state.get("permanentOtcMeds", [])) < 3:
        errors.append(f"Too few permanent OTC meds: {len(state.get('permanentOtcMeds', []))}")
    if len(state.get("pharmacies", [])) < 10:
        errors.append(f"Too few pharmacies: {len(state.get('pharmacies', []))}")
    if len(state.get("medicationDatabase", [])) < 50:
        errors.append(f"Too few medications in database: {len(state.get('medicationDatabase', []))}")

    # Validate medication fields
    for med in state.get("permanentRxMeds", []):
        if not med.get("id"):
            errors.append(f"Medication missing id: {med.get('medicationName')}")
        if not med.get("medicationName"):
            errors.append(f"Medication missing name: {med.get('id')}")
        if not med.get("sig"):
            errors.append(f"Medication missing sig: {med.get('id')}")

    # Validate pharmacy references
    pharm_ids = {p["id"] for p in state.get("pharmacies", [])}
    for med in state.get("permanentRxMeds", []):
        if med.get("pharmacyId") and med["pharmacyId"] not in pharm_ids:
            errors.append(f"Invalid pharmacyId {med['pharmacyId']} in med {med['id']}")

    # Validate refill request references
    med_ids = {m["id"] for m in state.get("permanentRxMeds", []) + state.get("permanentOtcMeds", []) + state.get("temporaryMeds", [])}
    for rr in state.get("refillRequests", []):
        if rr.get("patientMedId") and rr["patientMedId"] not in med_ids:
            # Some requests may reference discontinued meds
            disc_ids = {m["id"] for m in state.get("discontinuedMeds", [])}
            if rr["patientMedId"] not in disc_ids:
                errors.append(f"Invalid patientMedId {rr['patientMedId']} in refill request {rr['id']}")

    # Validate unique IDs
    all_med_ids = []
    for key in ["permanentRxMeds", "permanentOtcMeds", "temporaryMeds", "discontinuedMeds", "canceledScripts"]:
        for med in state.get(key, []):
            all_med_ids.append(med.get("id"))
    if len(all_med_ids) != len(set(all_med_ids)):
        dupes = [x for x in all_med_ids if all_med_ids.count(x) > 1]
        errors.append(f"Duplicate medication IDs: {set(dupes)}")

    return errors


def run_sanity_check(port=8099):
    """Run full sanity check."""
    print("Loading seed data...")
    seed_state = get_seed_state()

    print("Validating seed data structure...")
    errors = validate_seed_data(seed_state)
    if errors:
        print("SEED DATA ERRORS:")
        for e in errors:
            print(f"  - {e}")
        return False

    print("Seed data validation passed.")
    print(f"  Permanent Rx: {len(seed_state['permanentRxMeds'])}")
    print(f"  Permanent OTC: {len(seed_state['permanentOtcMeds'])}")
    print(f"  Temporary: {len(seed_state['temporaryMeds'])}")
    print(f"  Discontinued: {len(seed_state['discontinuedMeds'])}")
    print(f"  Canceled: {len(seed_state['canceledScripts'])}")
    print(f"  Pharmacies: {len(seed_state['pharmacies'])}")
    print(f"  Refill Requests: {len(seed_state['refillRequests'])}")
    print(f"  Rx Templates: {len(seed_state['rxTemplates'])}")
    print(f"  Medication DB: {len(seed_state['medicationDatabase'])}")
    print(f"  Drug Interactions: {len(seed_state['drugInteractions'])}")

    # Start server and test API
    print(f"\nStarting server on port {port}...")
    proc = subprocess.Popen(
        [sys.executable, str(APP_DIR / "server.py"), "--port", str(port)],
        cwd=str(APP_DIR),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(2)

    try:
        base_url = f"http://localhost:{port}"

        # PUT state
        print("Testing PUT /api/state...")
        r = requests.put(f"{base_url}/api/state", json=seed_state)
        assert r.status_code == 200, f"PUT failed: {r.status_code}"

        # GET state
        print("Testing GET /api/state...")
        r = requests.get(f"{base_url}/api/state")
        assert r.status_code == 200, f"GET failed: {r.status_code}"
        got_state = r.json()
        assert len(got_state["permanentRxMeds"]) == len(seed_state["permanentRxMeds"]), "permanentRxMeds count mismatch"

        # Test reset
        print("Testing POST /api/reset...")
        r = requests.post(f"{base_url}/api/reset")
        assert r.status_code == 200, f"Reset failed: {r.status_code}"
        reset_data = r.json()
        assert reset_data["seed_restored"] is True, "Seed not restored"

        # Verify reset state
        r = requests.get(f"{base_url}/api/state")
        reset_state = r.json()
        assert len(reset_state["permanentRxMeds"]) == len(seed_state["permanentRxMeds"]), "Reset did not restore meds"

        print("\nAll sanity checks passed!")
        return True

    except Exception as e:
        print(f"SANITY CHECK FAILED: {e}")
        return False
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    port = 8099
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        port = int(sys.argv[idx + 1])

    success = run_sanity_check(port)
    sys.exit(0 if success else 1)
