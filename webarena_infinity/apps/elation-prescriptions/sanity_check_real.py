#!/usr/bin/env python3
"""
Sanity check for real-tasks verifiers in the Elation Prescriptions app.

For each task, directly constructs the expected end-state (bypassing the UI),
writes it to the server, then runs the verifier and asserts it passes.
"""

import argparse
import importlib.util
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path

import requests

APP_DIR = Path(__file__).resolve().parent
TASKS_FILE = APP_DIR / "real-tasks.json"
SEED_LAST_RECONCILED = "2026-01-15T14:30:00Z"


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def get_seed_state():
    """Load seed data by evaluating data.js via Node."""
    data_js = APP_DIR / "js" / "data.js"
    node_script = r"""
    const fs = require('fs');
    const code = fs.readFileSync('%s', 'utf8');
    const fn = new Function(code + `; return {
        SEED_DATA_VERSION, CURRENT_USER, CURRENT_PATIENT,
        PERMANENT_RX_MEDS, PERMANENT_OTC_MEDS, TEMPORARY_MEDS,
        DISCONTINUED_MEDS, CANCELED_SCRIPTS, PHARMACIES,
        REFILL_REQUESTS, CHANGE_REQUESTS, RX_TEMPLATES,
        CUSTOM_SIGS, MEDICATION_DATABASE, DRUG_INTERACTIONS,
        FORMULARY_DATA, SETTINGS, PROVIDERS, DIAGNOSIS_CODES
    }`);
    const data = fn();
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


def find_entity(lst, **kwargs):
    """Find first entity matching all key=value pairs."""
    for item in lst:
        if all(item.get(k) == v for k, v in kwargs.items()):
            return item
    return None


def find_entity_containing(lst, field, substring):
    """Find first entity where field contains substring."""
    for item in lst:
        if substring.lower() in item.get(field, "").lower():
            return item
    return None


def remove_entity(lst, **kwargs):
    """Remove and return first entity matching criteria."""
    for i, item in enumerate(lst):
        if all(item.get(k) == v for k, v in kwargs.items()):
            return lst.pop(i)
    raise ValueError(f"Entity not found: {kwargs}")


def load_verifier(verify_path):
    full_path = str(APP_DIR / verify_path)
    spec = importlib.util.spec_from_file_location("verifier", full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.verify


def load_tasks():
    with open(TASKS_FILE) as f:
        return json.load(f)


NOW_DATE = "2026-03-06"
NOW_ISO = "2026-03-06T12:00:00.000Z"
CURRENT_USER_NAME = "Dr. Sarah Mitchell"
CURRENT_USER_ID = "prov_001"


# ──────────────────────────────────────────────
# Discontinue helper
# ──────────────────────────────────────────────

def _discontinue_med(state, med_name, source_list_key, reason, details="", send_cancel=False):
    """Helper: discontinue a medication."""
    med = remove_entity(state[source_list_key], medicationName=med_name)
    med["status"] = "discontinued"
    med["classification"] = "discontinued"
    med["discontinuedDate"] = NOW_DATE
    med["discontinuedBy"] = CURRENT_USER_NAME
    med["discontinueReason"] = reason
    med["discontinueDetails"] = details
    if send_cancel and med.get("pharmacyId"):
        cxl_id = f"cxl_{state['_nextCxlId']:03d}"
        state["canceledScripts"].append({
            "id": cxl_id,
            "medicationName": med["medicationName"],
            "ndc": med.get("ndc"),
            "sig": med["sig"],
            "qty": med["qty"],
            "refills": med.get("refills", 0),
            "daysSupply": med.get("daysSupply", 30),
            "status": "canceled",
            "classification": "canceled",
            "prescriberId": med.get("prescriberId"),
            "prescriberName": med.get("prescriberName"),
            "pharmacyId": med["pharmacyId"],
            "pharmacyName": med.get("pharmacyName"),
            "prescribedDate": med.get("lastPrescribedDate"),
            "canceledDate": NOW_DATE,
            "cancelReason": "Medication discontinued: " + reason,
            "diagnosis": med.get("diagnosis", [])
        })
        state["_nextCxlId"] += 1
    state["discontinuedMeds"].append(med)


def _add_prescription(state, med_name, sig, qty, unit, refills, days_supply,
                      classification, pharmacy_id, pharmacy_name,
                      diagnosis=None, is_controlled=False, schedule_class=None):
    """Helper: add a new prescription."""
    if classification == "temporary":
        pid = f"tmp_{state['_nextTmpId']:03d}"
        state["_nextTmpId"] += 1
    elif classification == "permanent_otc":
        pid = f"otc_{state['_nextOtcId']:03d}"
        state["_nextOtcId"] += 1
    else:
        pid = f"prx_{state['_nextPrxId']:03d}"
        state["_nextPrxId"] += 1

    med = {
        "id": pid,
        "medicationName": med_name,
        "ndc": None,
        "sig": sig,
        "qty": qty,
        "unit": unit,
        "refills": refills,
        "refillsRemaining": refills,
        "daysSupply": days_supply,
        "dispenseAsWritten": False,
        "status": "active",
        "classification": classification,
        "prescriberId": CURRENT_USER_ID,
        "prescriberName": CURRENT_USER_NAME,
        "pharmacyId": pharmacy_id,
        "pharmacyName": pharmacy_name,
        "startDate": NOW_DATE,
        "lastPrescribedDate": NOW_DATE,
        "lastFilledDate": None,
        "nextRefillDate": None,
        "diagnosis": diagnosis or [],
        "isControlled": is_controlled,
        "scheduleClass": schedule_class,
        "instructionsToPharmacy": "",
        "doNotFillBefore": None
    }

    if classification == "temporary":
        state["temporaryMeds"].append(med)
    elif classification == "permanent_otc":
        state["permanentOtcMeds"].append(med)
    else:
        state["permanentRxMeds"].append(med)
    return med


# ──────────────────────────────────────────────
# Solve functions — one per task
# Each takes seed state (deep copy) and mutates it
# ──────────────────────────────────────────────

# ── EASY ──

def solve_task_e1(state):
    """Approve Gabapentin refill request."""
    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    med = find_entity(state["permanentRxMeds"], medicationName="Gabapentin 300mg capsule")
    med["lastPrescribedDate"] = NOW_DATE


def solve_task_e2(state):
    """Deny Omeprazole refill request."""
    req = find_entity(state["refillRequests"], medicationName="Omeprazole 20mg capsule", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Patient needs follow-up before renewal"


def solve_task_e3(state):
    """Approve Atorvastatin→Rosuvastatin change request."""
    req = find_entity(state["changeRequests"], originalMedication="Atorvastatin 20mg tablet")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME


def solve_task_e4(state):
    """Remove Latex allergy."""
    allergies = state["currentPatient"]["allergies"]
    remove_entity(allergies, allergen="Latex")


def solve_task_e5(state):
    """Turn off drug-to-allergy alerts."""
    state["settings"]["drugDecisionSupport"]["drugToAllergyEnabled"] = False


def solve_task_e6(state):
    """Set drug interaction alerts to Major only."""
    state["settings"]["drugDecisionSupport"]["drugToDrugLevel"] = "major_only"


def solve_task_e7(state):
    """Disable cost estimates."""
    state["settings"]["showCostEstimates"] = False


def solve_task_e8(state):
    """Delete Prednisone taper Rx template."""
    remove_entity(state["rxTemplates"], medicationName="Prednisone 10mg tablet (taper)")


def solve_task_e9(state):
    """Discontinue Melatonin."""
    _discontinue_med(state, "Melatonin 3mg tablet", "permanentOtcMeds",
                     "I want to discontinue this medication")


def solve_task_e10(state):
    """Mark Montelukast as temporary."""
    med = remove_entity(state["permanentRxMeds"], medicationName="Montelukast 10mg tablet")
    med["classification"] = "temporary"
    state["temporaryMeds"].append(med)


def solve_task_e11(state):
    """Change default pharmacy to Walgreens #7892."""
    state["settings"]["defaultPharmacyId"] = "pharm_003"


def solve_task_e12(state):
    """Turn off auto-populate last used pharmacy."""
    state["settings"]["autoPopulateLastPharmacy"] = False


def solve_task_e13(state):
    """Delete custom sig 'Take 2 tablets by mouth once daily'."""
    remove_entity(state["customSigs"], text="Take 2 tablets by mouth once daily")


def solve_task_e14(state):
    """Remove Codeine allergy."""
    allergies = state["currentPatient"]["allergies"]
    remove_entity(allergies, allergen="Codeine")


def solve_task_e15(state):
    """Approve Sertraline refill."""
    req = find_entity(state["refillRequests"], medicationName="Sertraline 50mg tablet", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    med = find_entity(state["permanentRxMeds"], medicationName="Sertraline 50mg tablet")
    med["lastPrescribedDate"] = NOW_DATE


def solve_task_e16(state):
    """Turn off formulary information."""
    state["settings"]["showFormularyData"] = False


def solve_task_e17(state):
    """Delete Azithromycin Z-Pack template."""
    remove_entity(state["rxTemplates"], medicationName="Azithromycin 250mg tablet (Z-Pack)")


def solve_task_e18(state):
    """Deny Gabapentin sig clarification change request."""
    req = find_entity(state["changeRequests"], medicationName="Gabapentin 300mg capsule")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Current sig is correct as written"


def solve_task_e19(state):
    """Set Amoxicillin to permanent Rx."""
    med = remove_entity(state["temporaryMeds"], medicationName="Amoxicillin 500mg capsule")
    med["classification"] = "permanent_rx"
    state["permanentRxMeds"].append(med)


def solve_task_e20(state):
    """Approve Metoprolol refill."""
    req = find_entity(state["refillRequests"], medicationName="Metoprolol Succinate ER 50mg tablet", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    med = find_entity(state["permanentRxMeds"], medicationName="Metoprolol Succinate ER 50mg tablet")
    med["lastPrescribedDate"] = NOW_DATE


# ── MEDIUM ──

def solve_task_m1(state):
    """Add Ibuprofen drug allergy."""
    state["currentPatient"]["allergies"].append({
        "id": f"alg_{state['_nextAlgId']:03d}",
        "allergen": "Ibuprofen",
        "reaction": "GI bleeding",
        "severity": "Moderate",
        "type": "drug",
        "onsetDate": NOW_DATE,
        "source": "provider-entered"
    })
    state["_nextAlgId"] += 1


def solve_task_m2(state):
    """Document Glucosamine 1500mg OTC."""
    pid = f"otc_{state['_nextOtcId']:03d}"
    state["_nextOtcId"] += 1
    state["permanentOtcMeds"].append({
        "id": pid,
        "medicationName": "Glucosamine 1500mg tablet",
        "ndc": None,
        "sig": "Take 1 tablet by mouth once daily",
        "qty": 0,
        "unit": "tablets",
        "refills": 0,
        "refillsRemaining": 0,
        "daysSupply": 30,
        "dispenseAsWritten": False,
        "status": "active",
        "classification": "permanent_otc",
        "prescriberId": None,
        "prescriberName": None,
        "pharmacyId": None,
        "pharmacyName": None,
        "startDate": NOW_DATE,
        "lastPrescribedDate": None,
        "documentedDate": NOW_DATE,
        "diagnosis": [],
        "isControlled": False,
        "scheduleClass": None
    })


def solve_task_m3(state):
    """Discontinue Amoxicillin and send cancellation."""
    _discontinue_med(state, "Amoxicillin 500mg capsule", "temporaryMeds",
                     "I want to discontinue this medication", send_cancel=True)


def solve_task_m4(state):
    """Create Doxycycline 100mg Rx template."""
    tid = f"tpl_{state['_nextTplId']:03d}"
    state["_nextTplId"] += 1
    state["rxTemplates"].append({
        "id": tid,
        "medicationName": "Doxycycline 100mg capsule",
        "sig": "Take 1 capsule by mouth twice daily",
        "qty": 14,
        "unit": "capsules",
        "refills": 0,
        "daysSupply": 7,
        "ndc": None,
        "createdDate": NOW_DATE
    })


def solve_task_m5(state):
    """Add custom sig 'Take 2 capsules by mouth once daily with food'."""
    sid = f"sig_{state['_nextSigId']:03d}"
    state["_nextSigId"] += 1
    state["customSigs"].append({
        "id": sid,
        "text": "Take 2 capsules by mouth once daily with food",
        "category": "oral"
    })


def solve_task_m6(state):
    """Approve Gabapentin refill with modified sig."""
    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["modifications"] = {"sig": "Take 1 capsule by mouth twice daily"}
    med = find_entity(state["permanentRxMeds"], medicationName="Gabapentin 300mg capsule")
    med["sig"] = "Take 1 capsule by mouth twice daily"
    med["lastPrescribedDate"] = NOW_DATE


def solve_task_m7(state):
    """Deny Lisinopril refill."""
    req = find_entity(state["refillRequests"], medicationName="Lisinopril 10mg tablet", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Patient needs a follow-up blood pressure check first"


def solve_task_m8(state):
    """Discontinue Losartan — another prescriber."""
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "Discontinued by another prescriber")


def solve_task_m9(state):
    """Prescribe Levothyroxine 50mcg."""
    _add_prescription(state,
                      med_name="Levothyroxine 50mcg tablet",
                      sig="Take 1 tablet by mouth once daily on empty stomach",
                      qty=30, unit="tablets", refills=5, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521")


def solve_task_m10(state):
    """Update Metformin 1000mg template: qty 90, days supply 45."""
    tpl = find_entity(state["rxTemplates"], medicationName="Metformin 1000mg tablet")
    tpl["qty"] = 90
    tpl["daysSupply"] = 45


def solve_task_m11(state):
    """Add Shellfish food allergy."""
    state["currentPatient"]["allergies"].append({
        "id": f"alg_{state['_nextAlgId']:03d}",
        "allergen": "Shellfish",
        "reaction": "Hives, swelling",
        "severity": "Severe",
        "type": "food",
        "onsetDate": NOW_DATE,
        "source": "provider-entered"
    })
    state["_nextAlgId"] += 1


def solve_task_m12(state):
    """Deny Atorvastatin refill."""
    req = find_entity(state["refillRequests"], medicationName="Atorvastatin 20mg tablet", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Patient needs an updated lipid panel before renewal"


def solve_task_m13(state):
    """Prescribe Ondansetron 4mg temporary."""
    _add_prescription(state,
                      med_name="Ondansetron 4mg tablet",
                      sig="Take 1 tablet by mouth every 8 hours as needed for nausea",
                      qty=12, unit="tablets", refills=0, days_supply=30,
                      classification="temporary",
                      pharmacy_id=None, pharmacy_name=None)


def solve_task_m14(state):
    """Discontinue Prednisone taper."""
    _discontinue_med(state, "Prednisone 10mg tablet", "temporaryMeds",
                     "I want to discontinue this medication",
                     details="Patient completed the course")


def solve_task_m15(state):
    """Approve Metoprolol refill with refills=5."""
    req = find_entity(state["refillRequests"], medicationName="Metoprolol Succinate ER 50mg tablet", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["modifications"] = {"refills": 5}
    med = find_entity(state["permanentRxMeds"], medicationName="Metoprolol Succinate ER 50mg tablet")
    med["refillsRemaining"] = 5
    med["lastPrescribedDate"] = NOW_DATE


def solve_task_m16(state):
    """Set drug alerts to Major+Moderate, disable cost estimates."""
    state["settings"]["drugDecisionSupport"]["drugToDrugLevel"] = "major_moderate"
    state["settings"]["showCostEstimates"] = False


def solve_task_m17(state):
    """Add custom sig 'Apply to affected area three times daily' in topical."""
    sid = f"sig_{state['_nextSigId']:03d}"
    state["_nextSigId"] += 1
    state["customSigs"].append({
        "id": sid,
        "text": "Apply to affected area three times daily",
        "category": "topical"
    })


def solve_task_m18(state):
    """Move Ciprofloxacin to permanent Rx."""
    med = remove_entity(state["temporaryMeds"], medicationName="Ciprofloxacin 500mg tablet")
    med["classification"] = "permanent_rx"
    state["permanentRxMeds"].append(med)


def solve_task_m19(state):
    """Update Amlodipine template sig."""
    tpl = find_entity(state["rxTemplates"], medicationName="Amlodipine 5mg tablet")
    tpl["sig"] = "Take 1 tablet by mouth twice daily"


def solve_task_m20(state):
    """Prescribe Famotidine 20mg for GERD."""
    _add_prescription(state,
                      med_name="Famotidine 20mg tablet",
                      sig="Take 1 tablet by mouth once daily before dinner",
                      qty=30, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "K21.0", "description": "Gastroesophageal reflux disease"}])


# ── HARD ──

def solve_task_h1(state):
    """Approve all pending refill requests."""
    for req in state["refillRequests"]:
        if req["status"] == "pending":
            req["status"] = "approved"
            req["processedDate"] = NOW_ISO
            req["processedBy"] = CURRENT_USER_NAME
            if req.get("patientMedId"):
                med = find_entity(state["permanentRxMeds"], id=req["patientMedId"])
                if med:
                    med["lastPrescribedDate"] = NOW_DATE


def solve_task_h2(state):
    """Prescribe Buspirone 10mg to Walgreens (Sertraline's pharmacy)."""
    _add_prescription(state,
                      med_name="Buspirone 10mg tablet",
                      sig="Take 1 tablet by mouth once daily in the morning",
                      qty=30, unit="tablets", refills=5, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_003", pharmacy_name="Walgreens #7892",
                      diagnosis=[{"code": "F41.1", "description": "Generalized anxiety disorder"}])


def solve_task_h3(state):
    """Discontinue all temporary medications."""
    reason = "I want to discontinue this medication"
    for name in ["Amoxicillin 500mg capsule", "Prednisone 10mg tablet", "Ciprofloxacin 500mg tablet"]:
        _discontinue_med(state, name, "temporaryMeds", reason, details="Patient completed the course")


def solve_task_h4(state):
    """Med reconciliation — discontinue Calcium+D3."""
    _discontinue_med(state, "Calcium 600mg + Vitamin D3 400 IU tablet", "permanentOtcMeds",
                     "I want to discontinue this medication",
                     details="Discontinued during medication reconciliation")
    state["currentPatient"]["lastReconciledDate"] = NOW_ISO


def solve_task_h5(state):
    """Approve Atorvastatin substitution, prescribe Rosuvastatin 10mg."""
    req = find_entity(state["changeRequests"], originalMedication="Atorvastatin 20mg tablet")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    _add_prescription(state,
                      med_name="Rosuvastatin 10mg tablet",
                      sig="Take 1 tablet by mouth at bedtime",
                      qty=30, unit="tablets", refills=5, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "E78.5", "description": "Hyperlipidemia"}])


def solve_task_h6(state):
    """Move Ciprofloxacin to permanent, then refill at Rite Aid."""
    med = remove_entity(state["temporaryMeds"], medicationName="Ciprofloxacin 500mg tablet")
    med["classification"] = "permanent_rx"
    state["permanentRxMeds"].append(med)
    _add_prescription(state,
                      med_name="Ciprofloxacin 500mg tablet",
                      sig="Take 1 tablet by mouth twice daily for 7 days",
                      qty=14, unit="tablets", refills=0, days_supply=7,
                      classification="permanent_rx",
                      pharmacy_id="pharm_005", pharmacy_name="Rite Aid #3456")


def solve_task_h7(state):
    """Process all pending requests."""
    # Approve 5 refills
    for med_name in ["Lisinopril 10mg tablet", "Atorvastatin 20mg tablet",
                     "Omeprazole 20mg capsule", "Sertraline 50mg tablet",
                     "Metoprolol Succinate ER 50mg tablet"]:
        req = find_entity(state["refillRequests"], medicationName=med_name, status="pending")
        req["status"] = "approved"
        req["processedDate"] = NOW_ISO
        req["processedBy"] = CURRENT_USER_NAME
        if req.get("patientMedId"):
            med = find_entity(state["permanentRxMeds"], id=req["patientMedId"])
            if med:
                med["lastPrescribedDate"] = NOW_DATE

    # Deny Gabapentin refill
    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Patient needs an appointment"

    # Approve Atorvastatin change request
    cr = find_entity(state["changeRequests"], originalMedication="Atorvastatin 20mg tablet")
    cr["status"] = "approved"
    cr["processedDate"] = NOW_ISO
    cr["processedBy"] = CURRENT_USER_NAME

    # Deny Gabapentin change request
    cr2 = find_entity(state["changeRequests"], medicationName="Gabapentin 300mg capsule")
    cr2["status"] = "denied"
    cr2["processedDate"] = NOW_ISO
    cr2["processedBy"] = CURRENT_USER_NAME
    cr2["denyReason"] = "Current sig is correct"


def solve_task_h8(state):
    """Prescribe Albuterol inhaler to UCSF."""
    _add_prescription(state,
                      med_name="Albuterol 90mcg/actuation inhaler",
                      sig="Inhale 1-2 puffs every 4-6 hours as needed",
                      qty=1, unit="inhalers", refills=1, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_012", pharmacy_name="UCSF Medical Center Pharmacy",
                      diagnosis=[{"code": "J45.20", "description": "Mild intermittent asthma"}])


def solve_task_h9(state):
    """Deny both change requests."""
    cr1 = find_entity(state["changeRequests"], originalMedication="Atorvastatin 20mg tablet")
    cr1["status"] = "denied"
    cr1["processedDate"] = NOW_ISO
    cr1["processedBy"] = CURRENT_USER_NAME
    cr1["denyReason"] = "Current medication is working well"

    cr2 = find_entity(state["changeRequests"], medicationName="Gabapentin 300mg capsule")
    cr2["status"] = "denied"
    cr2["processedDate"] = NOW_ISO
    cr2["processedBy"] = CURRENT_USER_NAME
    cr2["denyReason"] = "Current sig is correct"


def solve_task_h10(state):
    """Discontinue Alprazolam with cancellation."""
    _discontinue_med(state, "Alprazolam 0.5mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Patient is transitioning to non-benzodiazepine anxiety management",
                     send_cancel=True)


def solve_task_h11(state):
    """Delete 4 Rx templates."""
    remove_entity(state["rxTemplates"], medicationName="Lisinopril 20mg tablet")
    remove_entity(state["rxTemplates"], medicationName="Metformin 1000mg tablet")
    remove_entity(state["rxTemplates"], medicationName="Atorvastatin 40mg tablet")
    remove_entity(state["rxTemplates"], medicationName="Azithromycin 250mg tablet (Z-Pack)")


def solve_task_h12(state):
    """Create Doxycycline and Cephalexin templates."""
    tid1 = f"tpl_{state['_nextTplId']:03d}"
    state["_nextTplId"] += 1
    state["rxTemplates"].append({
        "id": tid1,
        "medicationName": "Doxycycline 100mg capsule",
        "sig": "Take 1 capsule by mouth twice daily",
        "qty": 20,
        "unit": "capsules",
        "refills": 0,
        "daysSupply": 10,
        "ndc": None,
        "createdDate": NOW_DATE
    })
    tid2 = f"tpl_{state['_nextTplId']:03d}"
    state["_nextTplId"] += 1
    state["rxTemplates"].append({
        "id": tid2,
        "medicationName": "Cephalexin 500mg capsule",
        "sig": "Take 1 capsule by mouth three times daily",
        "qty": 21,
        "unit": "capsules",
        "refills": 0,
        "daysSupply": 7,
        "ndc": None,
        "createdDate": NOW_DATE
    })


def solve_task_h13(state):
    """Approve Sertraline refill, prescribe Sertraline 100mg at Walgreens."""
    req = find_entity(state["refillRequests"], medicationName="Sertraline 50mg tablet", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    med = find_entity(state["permanentRxMeds"], medicationName="Sertraline 50mg tablet")
    med["lastPrescribedDate"] = NOW_DATE

    _add_prescription(state,
                      med_name="Sertraline 100mg tablet",
                      sig="Take 1 tablet by mouth once daily in the morning",
                      qty=30, unit="tablets", refills=5, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_003", pharmacy_name="Walgreens #7892",
                      diagnosis=[{"code": "F41.1", "description": "Generalized anxiety disorder"}])


def solve_task_h14(state):
    """Change default pharmacy, prescribe Gabapentin refill, turn off auto-populate."""
    state["settings"]["defaultPharmacyId"] = "pharm_003"
    state["settings"]["autoPopulateLastPharmacy"] = False
    _add_prescription(state,
                      med_name="Gabapentin 300mg capsule",
                      sig="Take 1 capsule by mouth three times daily",
                      qty=90, unit="capsules", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_003", pharmacy_name="Walgreens #7892",
                      diagnosis=[{"code": "M54.5", "description": "Chronic low back pain"}])


def solve_task_h15(state):
    """Discontinue Losartan and Amlodipine, prescribe Valsartan 160mg."""
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication")
    _discontinue_med(state, "Amlodipine 5mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication")
    _add_prescription(state,
                      med_name="Valsartan 160mg tablet",
                      sig="Take 1 tablet by mouth once daily",
                      qty=30, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "I10", "description": "Essential hypertension"}])


def solve_task_h16(state):
    """Approve Lisinopril, Atorvastatin, Sertraline; deny Gabapentin."""
    for med_name in ["Lisinopril 10mg tablet", "Atorvastatin 20mg tablet", "Sertraline 50mg tablet"]:
        req = find_entity(state["refillRequests"], medicationName=med_name, status="pending")
        req["status"] = "approved"
        req["processedDate"] = NOW_ISO
        req["processedBy"] = CURRENT_USER_NAME
        if req.get("patientMedId"):
            med = find_entity(state["permanentRxMeds"], id=req["patientMedId"])
            if med:
                med["lastPrescribedDate"] = NOW_DATE

    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Patient needs an appointment"


def solve_task_h17(state):
    """Add Peanut allergy, prescribe Doxycycline 100mg temporary."""
    state["currentPatient"]["allergies"].append({
        "id": f"alg_{state['_nextAlgId']:03d}",
        "allergen": "Peanut",
        "reaction": "Anaphylaxis",
        "severity": "Severe",
        "type": "food",
        "onsetDate": NOW_DATE,
        "source": "provider-entered"
    })
    state["_nextAlgId"] += 1

    _add_prescription(state,
                      med_name="Doxycycline 100mg capsule",
                      sig="Take 1 capsule by mouth twice daily for 10 days",
                      qty=20, unit="capsules", refills=0, days_supply=10,
                      classification="temporary",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521")


def solve_task_h18(state):
    """Delete both Lisinopril templates, create Losartan template."""
    remove_entity(state["rxTemplates"], medicationName="Lisinopril 10mg tablet")
    remove_entity(state["rxTemplates"], medicationName="Lisinopril 20mg tablet")
    tid = f"tpl_{state['_nextTplId']:03d}"
    state["_nextTplId"] += 1
    state["rxTemplates"].append({
        "id": tid,
        "medicationName": "Losartan 50mg tablet",
        "sig": "Take 1 tablet by mouth once daily",
        "qty": 30,
        "unit": "tablets",
        "refills": 3,
        "daysSupply": 30,
        "ndc": None,
        "createdDate": NOW_DATE
    })


def solve_task_h19(state):
    """Discontinue Omeprazole, prescribe Famotidine 20mg BID."""
    _discontinue_med(state, "Omeprazole 20mg capsule", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Switching to Famotidine")
    _add_prescription(state,
                      med_name="Famotidine 20mg tablet",
                      sig="Take 1 tablet by mouth twice daily",
                      qty=60, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "K21.0", "description": "Gastroesophageal reflux disease"}])


def solve_task_h20(state):
    """Med reconciliation — discontinue Centrum Silver and Melatonin."""
    _discontinue_med(state, "Centrum Silver Multivitamin tablet", "permanentOtcMeds",
                     "I want to discontinue this medication",
                     details="Discontinued during medication reconciliation")
    _discontinue_med(state, "Melatonin 3mg tablet", "permanentOtcMeds",
                     "I want to discontinue this medication",
                     details="Discontinued during medication reconciliation")
    state["currentPatient"]["lastReconciledDate"] = NOW_ISO


# ── HARD (hardening round 1) ──

def solve_task_h21(state):
    """Discontinue controlled substance (Alprazolam), cancel, prescribe Hydroxyzine."""
    _discontinue_med(state, "Alprazolam 0.5mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Patient is transitioning to non-controlled alternatives",
                     send_cancel=True)
    _add_prescription(state,
                      med_name="Hydroxyzine 25mg tablet",
                      sig="Take 1 tablet by mouth twice daily as needed",
                      qty=60, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521")


def solve_task_h22(state):
    """Deny Omeprazole refill, discontinue, prescribe Pantoprazole."""
    req = find_entity(state["refillRequests"], medicationName="Omeprazole 20mg capsule", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Switching to a different medication"

    _discontinue_med(state, "Omeprazole 20mg capsule", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Switching to Pantoprazole")

    _add_prescription(state,
                      med_name="Pantoprazole 40mg tablet",
                      sig="Take 1 tablet by mouth once daily before breakfast",
                      qty=30, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "K21.0", "description": "Gastroesophageal reflux disease"}])


def solve_task_h23(state):
    """Med rec: discontinue Fish Oil, document Turmeric OTC."""
    _discontinue_med(state, "Fish Oil 1000mg softgel", "permanentOtcMeds",
                     "I want to discontinue this medication",
                     details="Discontinued during medication reconciliation")
    state["currentPatient"]["lastReconciledDate"] = NOW_ISO

    pid = f"otc_{state['_nextOtcId']:03d}"
    state["_nextOtcId"] += 1
    state["permanentOtcMeds"].append({
        "id": pid,
        "medicationName": "Turmeric 500mg capsule",
        "ndc": None,
        "sig": "Take 1 capsule by mouth once daily with food",
        "qty": 0,
        "unit": "capsules",
        "refills": 0,
        "refillsRemaining": 0,
        "daysSupply": 30,
        "dispenseAsWritten": False,
        "status": "active",
        "classification": "permanent_otc",
        "prescriberId": None,
        "prescriberName": None,
        "pharmacyId": None,
        "pharmacyName": None,
        "startDate": NOW_DATE,
        "lastPrescribedDate": None,
        "documentedDate": NOW_DATE,
        "diagnosis": [],
        "isControlled": False,
        "scheduleClass": None
    })


def solve_task_h24(state):
    """Discontinue ARB (Losartan) with cancellation."""
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     send_cancel=True)


def solve_task_h25(state):
    """Delete oral capsule custom sigs."""
    capsule_sigs = [
        "Take 1 capsule by mouth once daily",
        "Take 1 capsule by mouth twice daily",
        "Take 1 capsule by mouth three times daily",
        "Take 1 capsule by mouth once daily before breakfast",
    ]
    for sig_text in capsule_sigs:
        remove_entity(state["customSigs"], text=sig_text)


def solve_task_h26(state):
    """Approve Atorvastatin refill, create Rosuvastatin template."""
    req = find_entity(state["refillRequests"], medicationName="Atorvastatin 20mg tablet", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    med = find_entity(state["permanentRxMeds"], medicationName="Atorvastatin 20mg tablet")
    med["lastPrescribedDate"] = NOW_DATE

    tid = f"tpl_{state['_nextTplId']:03d}"
    state["_nextTplId"] += 1
    state["rxTemplates"].append({
        "id": tid,
        "medicationName": "Rosuvastatin 10mg tablet",
        "sig": "Take 1 tablet by mouth at bedtime",
        "qty": 30,
        "unit": "tablets",
        "refills": 5,
        "daysSupply": 30,
        "ndc": None,
        "createdDate": NOW_DATE
    })


def solve_task_h27(state):
    """Approve Metoprolol (beta-blocker) refill with sig modification."""
    req = find_entity(state["refillRequests"], medicationName="Metoprolol Succinate ER 50mg tablet", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["modifications"] = {"sig": "Take 1 tablet by mouth once daily in the morning"}
    med = find_entity(state["permanentRxMeds"], medicationName="Metoprolol Succinate ER 50mg tablet")
    med["sig"] = "Take 1 tablet by mouth once daily in the morning"
    med["lastPrescribedDate"] = NOW_DATE


def solve_task_h28(state):
    """Add Tramadol allergy, set drug alerts to Major only."""
    state["currentPatient"]["allergies"].append({
        "id": f"alg_{state['_nextAlgId']:03d}",
        "allergen": "Tramadol",
        "reaction": "Seizures",
        "severity": "Severe",
        "type": "drug",
        "onsetDate": NOW_DATE,
        "source": "provider-entered"
    })
    state["_nextAlgId"] += 1
    state["settings"]["drugDecisionSupport"]["drugToDrugLevel"] = "major_only"


def solve_task_h29(state):
    """Approve Walgreens refill (Sertraline) with refills=11, change default pharmacy."""
    req = find_entity(state["refillRequests"], medicationName="Sertraline 50mg tablet", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["modifications"] = {"refills": 11}
    med = find_entity(state["permanentRxMeds"], medicationName="Sertraline 50mg tablet")
    med["refillsRemaining"] = 11
    med["lastPrescribedDate"] = NOW_DATE
    state["settings"]["defaultPharmacyId"] = "pharm_003"


def solve_task_h30(state):
    """Disc Prednisone+Amoxicillin, move Ciprofloxacin to permanent."""
    _discontinue_med(state, "Prednisone 10mg tablet", "temporaryMeds",
                     "I want to discontinue this medication",
                     details="Patient completed the course")
    _discontinue_med(state, "Amoxicillin 500mg capsule", "temporaryMeds",
                     "I want to discontinue this medication",
                     details="Patient completed the course")
    med = remove_entity(state["temporaryMeds"], medicationName="Ciprofloxacin 500mg tablet")
    med["classification"] = "permanent_rx"
    state["permanentRxMeds"].append(med)


def solve_task_h31(state):
    """Create Amlodipine 10mg template, delete 5mg template."""
    tid = f"tpl_{state['_nextTplId']:03d}"
    state["_nextTplId"] += 1
    state["rxTemplates"].append({
        "id": tid,
        "medicationName": "Amlodipine 10mg tablet",
        "sig": "Take 1 tablet by mouth once daily",
        "qty": 30,
        "unit": "tablets",
        "refills": 3,
        "daysSupply": 30,
        "ndc": None,
        "createdDate": NOW_DATE
    })
    remove_entity(state["rxTemplates"], medicationName="Amlodipine 5mg tablet")


def solve_task_h32(state):
    """Discontinue DAW Losartan, prescribe replacement without DAW."""
    losartan = find_entity(state["permanentRxMeds"], medicationName="Losartan 50mg tablet")
    orig_sig = losartan["sig"]
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication")
    _add_prescription(state,
                      med_name="Losartan 50mg tablet",
                      sig=orig_sig,
                      qty=30, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_003", pharmacy_name="Walgreens #7892",
                      diagnosis=[{"code": "I10", "description": "Essential hypertension"}])


def solve_task_h33(state):
    """Set alerts to Major only, disable cost estimates, prescribe Cyclobenzaprine."""
    state["settings"]["drugDecisionSupport"]["drugToDrugLevel"] = "major_only"
    state["settings"]["showCostEstimates"] = False
    _add_prescription(state,
                      med_name="Cyclobenzaprine 10mg tablet",
                      sig="Take 1 tablet by mouth three times daily",
                      qty=30, unit="tablets", refills=1, days_supply=10,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "M54.5", "description": "Chronic low back pain"}])


def solve_task_h34(state):
    """Approve Sertraline refill (Walgreens anxiety med), discontinue Losartan (Walgreens other provider)."""
    req = find_entity(state["refillRequests"], medicationName="Sertraline 50mg tablet", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    med = find_entity(state["permanentRxMeds"], medicationName="Sertraline 50mg tablet")
    med["lastPrescribedDate"] = NOW_DATE

    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "Discontinued by another prescriber")


def solve_task_h35(state):
    """Remove Penicillin allergy, prescribe Amoxicillin 875mg temporary."""
    remove_entity(state["currentPatient"]["allergies"], allergen="Penicillin")
    _add_prescription(state,
                      med_name="Amoxicillin 875mg capsule",
                      sig="Take 1 capsule by mouth twice daily for 10 days",
                      qty=20, unit="capsules", refills=0, days_supply=10,
                      classification="temporary",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "J01.90", "description": "Acute sinusitis, unspecified"}])


def solve_task_h36(state):
    """Delete templates for non-current permanent Rx meds."""
    to_delete = [
        "Lisinopril 20mg tablet",
        "Metformin 1000mg tablet",
        "Atorvastatin 40mg tablet",
        "Amoxicillin 500mg capsule",
        "Azithromycin 250mg tablet (Z-Pack)",
        "Prednisone 10mg tablet (taper)",
    ]
    for name in to_delete:
        remove_entity(state["rxTemplates"], medicationName=name)


def solve_task_h37(state):
    """Approve Gabapentin refill (has notes), deny all others."""
    # Gabapentin has notes — approve
    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    med = find_entity(state["permanentRxMeds"], medicationName="Gabapentin 300mg capsule")
    med["lastPrescribedDate"] = NOW_DATE

    # All others have no notes — deny
    deny_reason = "Routine refill — schedule office visit for renewal"
    for med_name in ["Lisinopril 10mg tablet", "Atorvastatin 20mg tablet",
                     "Omeprazole 20mg capsule", "Sertraline 50mg tablet",
                     "Metoprolol Succinate ER 50mg tablet"]:
        r = find_entity(state["refillRequests"], medicationName=med_name, status="pending")
        r["status"] = "denied"
        r["processedDate"] = NOW_ISO
        r["processedBy"] = CURRENT_USER_NAME
        r["denyReason"] = deny_reason


def solve_task_h38(state):
    """Remove Sulfonamides allergy, prescribe TMP-SMX temporary."""
    remove_entity(state["currentPatient"]["allergies"], allergen="Sulfonamides")
    _add_prescription(state,
                      med_name="Trimethoprim-Sulfamethoxazole 800mg/160mg tablet",
                      sig="Take 1 tablet by mouth twice daily for 7 days",
                      qty=14, unit="tablets", refills=0, days_supply=7,
                      classification="temporary",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "N39.0", "description": "Urinary tract infection"}])


def solve_task_h39(state):
    """Change default to Express Scripts, document Magnesium OTC."""
    state["settings"]["defaultPharmacyId"] = "pharm_011"

    pid = f"otc_{state['_nextOtcId']:03d}"
    state["_nextOtcId"] += 1
    state["permanentOtcMeds"].append({
        "id": pid,
        "medicationName": "Magnesium Citrate 400mg tablet",
        "ndc": None,
        "sig": "Take 1 tablet by mouth once daily at bedtime",
        "qty": 0,
        "unit": "tablets",
        "refills": 0,
        "refillsRemaining": 0,
        "daysSupply": 30,
        "dispenseAsWritten": False,
        "status": "active",
        "classification": "permanent_otc",
        "prescriberId": None,
        "prescriberName": None,
        "pharmacyId": None,
        "pharmacyName": None,
        "startDate": NOW_DATE,
        "lastPrescribedDate": None,
        "documentedDate": NOW_DATE,
        "diagnosis": [],
        "isControlled": False,
        "scheduleClass": None
    })


def solve_task_h40(state):
    """Transfer Metformin to Express Scripts mail-order."""
    metformin = find_entity(state["permanentRxMeds"], medicationName="Metformin 500mg tablet")
    orig_sig = metformin["sig"]
    _discontinue_med(state, "Metformin 500mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Transferring to mail-order pharmacy")
    _add_prescription(state,
                      med_name="Metformin 500mg tablet",
                      sig=orig_sig,
                      qty=180, unit="tablets", refills=5, days_supply=90,
                      classification="permanent_rx",
                      pharmacy_id="pharm_011",
                      pharmacy_name="Express Scripts Mail Pharmacy",
                      diagnosis=[{"code": "E11.9", "description": "Type 2 diabetes mellitus"}])


# ── HARD (Hardening Round 2) ──

def solve_task_h41(state):
    """Change default pharmacy to Walgreens (Dr. Chen's Losartan pharmacy)."""
    state["settings"]["defaultPharmacyId"] = "pharm_003"


def solve_task_h42(state):
    """Approve CVS refills, deny non-CVS refills."""
    # CVS pending refills
    for med_name in ["Lisinopril 10mg tablet", "Atorvastatin 20mg tablet",
                     "Gabapentin 300mg capsule", "Omeprazole 20mg capsule",
                     "Metoprolol Succinate ER 50mg tablet"]:
        req = find_entity(state["refillRequests"], medicationName=med_name, status="pending")
        req["status"] = "approved"
        req["processedDate"] = NOW_ISO
        req["processedBy"] = CURRENT_USER_NAME
        med = find_entity(state["permanentRxMeds"], medicationName=med_name)
        med["lastPrescribedDate"] = NOW_DATE

    # Non-CVS pending refill (Sertraline at Walgreens)
    req = find_entity(state["refillRequests"], medicationName="Sertraline 50mg tablet", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Please transfer prescription to CVS"


def solve_task_h43(state):
    """Discontinue both Walgreens meds (Losartan, Sertraline) with cancellations."""
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication", send_cancel=True)
    _discontinue_med(state, "Sertraline 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication", send_cancel=True)


def solve_task_h44(state):
    """Approve Gabapentin refill (0 refills remaining, non-controlled) with refills=3."""
    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["modifications"] = {"refills": 3}
    med = find_entity(state["permanentRxMeds"], medicationName="Gabapentin 300mg capsule")
    med["refillsRemaining"] = 3
    med["lastPrescribedDate"] = NOW_DATE


def solve_task_h45(state):
    """Delete all PRN sigs, add new nausea PRN sig."""
    prn_sigs = [s for s in state["customSigs"] if s.get("category") == "prn"]
    for sig in prn_sigs:
        state["customSigs"].remove(sig)

    sid = f"sig_{state['_nextSigId']:03d}"
    state["_nextSigId"] += 1
    state["customSigs"].append({
        "id": sid,
        "text": "Take 1 tablet by mouth every 4-6 hours as needed for nausea",
        "category": "prn"
    })


def solve_task_h46(state):
    """Med rec: discontinue OTC meds with no prescriber."""
    no_prescriber = [
        "Fish Oil 1000mg softgel",
        "Calcium 600mg + Vitamin D3 400 IU tablet",
        "Centrum Silver Multivitamin tablet",
        "Melatonin 3mg tablet",
    ]
    for name in no_prescriber:
        _discontinue_med(state, name, "permanentOtcMeds",
                         "I want to discontinue this medication",
                         details="Discontinued during medication reconciliation")
    state["currentPatient"]["lastReconciledDate"] = NOW_ISO


def solve_task_h47(state):
    """Prescribe Sertraline refill at CVS instead of Walgreens."""
    _add_prescription(state,
                      med_name="Sertraline 50mg tablet",
                      sig="Take 1 tablet by mouth once daily in the morning",
                      qty=30, unit="tablets", refills=5, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "F41.1", "description": "Generalized anxiety disorder"}])


def solve_task_h48(state):
    """Create Rx templates for all 3 temporary meds."""
    temp_meds = [
        {"medicationName": "Amoxicillin 500mg capsule",
         "sig": "Take 1 capsule by mouth three times daily for 10 days",
         "qty": 30, "unit": "capsules", "daysSupply": 10},
        {"medicationName": "Prednisone 10mg tablet",
         "sig": "Take as directed: 4 tabs day 1-2, 3 tabs day 3-4, 2 tabs day 5-6, 1 tab day 7",
         "qty": 21, "unit": "tablets", "daysSupply": 7},
        {"medicationName": "Ciprofloxacin 500mg tablet",
         "sig": "Take 1 tablet by mouth twice daily for 7 days",
         "qty": 14, "unit": "tablets", "daysSupply": 7},
    ]
    for tm in temp_meds:
        tid = f"tpl_{state['_nextTplId']:03d}"
        state["_nextTplId"] += 1
        state["rxTemplates"].append({
            "id": tid,
            "medicationName": tm["medicationName"],
            "sig": tm["sig"],
            "qty": tm["qty"],
            "unit": tm["unit"],
            "refills": 0,
            "daysSupply": tm["daysSupply"],
            "ndc": None,
            "createdDate": NOW_DATE
        })


def solve_task_h49(state):
    """Approve Atorvastatin substitution, deny Gabapentin clarification."""
    cr = find_entity(state["changeRequests"], originalMedication="Atorvastatin 20mg tablet")
    cr["status"] = "approved"
    cr["processedDate"] = NOW_ISO
    cr["processedBy"] = CURRENT_USER_NAME

    cr2 = find_entity(state["changeRequests"], medicationName="Gabapentin 300mg capsule")
    cr2["status"] = "denied"
    cr2["processedDate"] = NOW_ISO
    cr2["processedBy"] = CURRENT_USER_NAME
    cr2["denyReason"] = "Current TID dosing is correct as prescribed"


def solve_task_h50(state):
    """Deny Atorvastatin (lipid panel) and Lisinopril (BP follow-up) refills."""
    req = find_entity(state["refillRequests"], medicationName="Atorvastatin 20mg tablet", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Lipid panel overdue — needs updated labs before renewal"

    req2 = find_entity(state["refillRequests"], medicationName="Lisinopril 10mg tablet", status="pending")
    req2["status"] = "denied"
    req2["processedDate"] = NOW_ISO
    req2["processedBy"] = CURRENT_USER_NAME
    req2["denyReason"] = "Needs follow-up blood pressure check before renewal"


def solve_task_h51(state):
    """Discontinue Losartan (more recent, major interaction with Lisinopril)."""
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Major drug-drug interaction with Lisinopril (ACE-I + ARB)",
                     send_cancel=True)


def solve_task_h52(state):
    """Approve Gabapentin refill with BID sig + 5 refills, approve change request."""
    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["modifications"] = {"sig": "Take 1 capsule by mouth twice daily", "refills": 5}
    med = find_entity(state["permanentRxMeds"], medicationName="Gabapentin 300mg capsule")
    med["sig"] = "Take 1 capsule by mouth twice daily"
    med["refillsRemaining"] = 5
    med["lastPrescribedDate"] = NOW_DATE

    cr = find_entity(state["changeRequests"], medicationName="Gabapentin 300mg capsule")
    cr["status"] = "approved"
    cr["processedDate"] = NOW_ISO
    cr["processedBy"] = CURRENT_USER_NAME


def solve_task_h53(state):
    """Discontinue Lisinopril+Losartan with cancellations, prescribe Amlodipine 10mg."""
    _discontinue_med(state, "Lisinopril 10mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Consolidating BP meds", send_cancel=True)
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Consolidating BP meds", send_cancel=True)
    _add_prescription(state,
                      med_name="Amlodipine 10mg tablet",
                      sig="Take 1 tablet by mouth once daily",
                      qty=30, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "I10", "description": "Essential hypertension"}])


def solve_task_h54(state):
    """Delete templates not matching active permanent Rx strengths."""
    to_delete = [
        "Lisinopril 20mg tablet",
        "Metformin 1000mg tablet",
        "Atorvastatin 40mg tablet",
        "Amoxicillin 500mg capsule",
        "Azithromycin 250mg tablet (Z-Pack)",
        "Prednisone 10mg tablet (taper)",
    ]
    for name in to_delete:
        remove_entity(state["rxTemplates"], medicationName=name)


def solve_task_h55(state):
    """Add Morphine allergy, disable allergy alerts, set interactions to Major only."""
    state["currentPatient"]["allergies"].append({
        "id": f"alg_{state['_nextAlgId']:03d}",
        "allergen": "Morphine",
        "reaction": "Respiratory depression",
        "severity": "Severe",
        "type": "drug",
        "onsetDate": NOW_DATE,
        "source": "provider-entered"
    })
    state["_nextAlgId"] += 1
    state["settings"]["drugDecisionSupport"]["drugToAllergyEnabled"] = False
    state["settings"]["drugDecisionSupport"]["drugToDrugLevel"] = "major_only"


def solve_task_h56(state):
    """Move Ciprofloxacin to permanent Rx, deny Gabapentin clarification."""
    med = remove_entity(state["temporaryMeds"], medicationName="Ciprofloxacin 500mg tablet")
    med["classification"] = "permanent_rx"
    state["permanentRxMeds"].append(med)

    cr = find_entity(state["changeRequests"], medicationName="Gabapentin 300mg capsule")
    cr["status"] = "denied"
    cr["processedDate"] = NOW_ISO
    cr["processedBy"] = CURRENT_USER_NAME
    cr["denyReason"] = "Current sig is correct as written"


def solve_task_h57(state):
    """Bulk refill Lisinopril and Metformin at CVS with 90-day supply."""
    lisinopril = find_entity(state["permanentRxMeds"], medicationName="Lisinopril 10mg tablet")
    _add_prescription(state,
                      med_name="Lisinopril 10mg tablet",
                      sig=lisinopril["sig"],
                      qty=90, unit="tablets", refills=5, days_supply=90,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "I10", "description": "Essential hypertension"}])

    metformin = find_entity(state["permanentRxMeds"], medicationName="Metformin 500mg tablet")
    _add_prescription(state,
                      med_name="Metformin 500mg tablet",
                      sig=metformin["sig"],
                      qty=90, unit="tablets", refills=5, days_supply=90,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "E11.9", "description": "Type 2 diabetes mellitus"}])


def solve_task_h58(state):
    """Remove Penicillin+Codeine allergies, add Erythromycin allergy."""
    remove_entity(state["currentPatient"]["allergies"], allergen="Penicillin")
    remove_entity(state["currentPatient"]["allergies"], allergen="Codeine")
    state["currentPatient"]["allergies"].append({
        "id": f"alg_{state['_nextAlgId']:03d}",
        "allergen": "Erythromycin",
        "reaction": "QT prolongation",
        "severity": "Severe",
        "type": "drug",
        "onsetDate": NOW_DATE,
        "source": "provider-entered"
    })
    state["_nextAlgId"] += 1


def solve_task_h59(state):
    """Discontinue Omeprazole+Melatonin, prescribe Famotidine 40mg."""
    _discontinue_med(state, "Omeprazole 20mg capsule", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Switching to Famotidine")
    _discontinue_med(state, "Melatonin 3mg tablet", "permanentOtcMeds",
                     "I want to discontinue this medication")
    _add_prescription(state,
                      med_name="Famotidine 40mg tablet",
                      sig="Take 1 tablet by mouth once daily before dinner",
                      qty=30, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "K21.0", "description": "Gastroesophageal reflux disease"}])


def solve_task_h60(state):
    """Set default pharmacy to Rite Aid (Ciprofloxacin's pharmacy), disable settings."""
    state["settings"]["defaultPharmacyId"] = "pharm_005"
    state["settings"]["autoPopulateLastPharmacy"] = False
    state["settings"]["showFormularyData"] = False


# ── HARD (Hardening Round 3) ──

def solve_task_h61(state):
    """Approve all pending refills; for meds with 0 refills remaining, set refills=3."""
    for req in state["refillRequests"]:
        if req["status"] != "pending":
            continue
        req["status"] = "approved"
        req["processedDate"] = NOW_ISO
        req["processedBy"] = CURRENT_USER_NAME
        # Find the underlying medication
        med = find_entity(state["permanentRxMeds"], medicationName=req["medicationName"])
        if med:
            if med.get("refillsRemaining", 0) == 0:
                req["modifications"] = {"refills": 3}
                med["refillsRemaining"] = 3
            med["lastPrescribedDate"] = NOW_DATE


def solve_task_h62(state):
    """Prescribe 90-day Gabapentin (most overdue med) at CVS."""
    gaba = find_entity(state["permanentRxMeds"], medicationName="Gabapentin 300mg capsule")
    _add_prescription(state,
                      med_name="Gabapentin 300mg capsule",
                      sig=gaba["sig"],
                      qty=90, unit="capsules", refills=5, days_supply=90,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "M54.5", "description": "Chronic low back pain"}])


def solve_task_h63(state):
    """Discontinue Alprazolam (controlled anxiety med), prescribe Buspirone at same pharmacy."""
    _discontinue_med(state, "Alprazolam 0.5mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Transitioning to non-controlled anxiolytic",
                     send_cancel=True)
    _add_prescription(state,
                      med_name="Buspirone 15mg tablet",
                      sig="Take 1 tablet by mouth twice daily",
                      qty=60, unit="tablets", refills=5, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "F41.1", "description": "Generalized anxiety disorder"}])


def solve_task_h64(state):
    """Prescribe Duloxetine 60mg with DAW and dual diagnoses."""
    med = _add_prescription(state,
                            med_name="Duloxetine 60mg capsule",
                            sig="Take 1 capsule by mouth once daily",
                            qty=30, unit="capsules", refills=5, days_supply=30,
                            classification="permanent_rx",
                            pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                            diagnosis=[
                                {"code": "M54.5", "description": "Chronic low back pain"},
                                {"code": "F41.1", "description": "Generalized anxiety disorder"}
                            ])
    med["dispenseAsWritten"] = True


def solve_task_h65(state):
    """Med rec: discontinue Calcium+D3 combo (redundant vitamin D)."""
    _discontinue_med(state, "Calcium 600mg + Vitamin D3 400 IU tablet", "permanentOtcMeds",
                     "I want to discontinue this medication",
                     details="Discontinued during medication reconciliation — redundant vitamin D")
    state["currentPatient"]["lastReconciledDate"] = NOW_ISO


def solve_task_h66(state):
    """Approve most recently submitted refill (Metoprolol), deny all others."""
    for req in state["refillRequests"]:
        if req["status"] != "pending":
            continue
        req["processedDate"] = NOW_ISO
        req["processedBy"] = CURRENT_USER_NAME
        if req["medicationName"] == "Metoprolol Succinate ER 50mg tablet":
            req["status"] = "approved"
            med = find_entity(state["permanentRxMeds"], medicationName=req["medicationName"])
            if med:
                med["lastPrescribedDate"] = NOW_DATE
        else:
            req["status"] = "denied"
            req["denyReason"] = "Batch processing — please resubmit next week"


def solve_task_h67(state):
    """Discontinue Losartan (ARB, drug interaction), prescribe Lisinopril 20mg step-up."""
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Major drug interaction with Lisinopril (ACE + ARB)",
                     send_cancel=True)
    _add_prescription(state,
                      med_name="Lisinopril 20mg tablet",
                      sig="Take 1 tablet by mouth once daily",
                      qty=30, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "I10", "description": "Essential hypertension"}])


def solve_task_h68(state):
    """Edit Omeprazole template (sig + refills), delete Sertraline template."""
    tpl = find_entity(state["rxTemplates"], medicationName="Omeprazole 20mg capsule")
    tpl["sig"] = "Take 1 capsule by mouth twice daily before meals"
    tpl["refills"] = 5
    remove_entity(state["rxTemplates"], medicationName="Sertraline 50mg tablet")


def solve_task_h69(state):
    """Approve all refills except Lisinopril (major interaction with Losartan)."""
    for req in state["refillRequests"]:
        if req["status"] != "pending":
            continue
        req["processedDate"] = NOW_ISO
        req["processedBy"] = CURRENT_USER_NAME
        if req["medicationName"] == "Lisinopril 10mg tablet":
            req["status"] = "denied"
            req["denyReason"] = "Drug interaction — needs provider review before renewal"
        else:
            req["status"] = "approved"
            med = find_entity(state["permanentRxMeds"], medicationName=req["medicationName"])
            if med:
                med["lastPrescribedDate"] = NOW_DATE


def solve_task_h70(state):
    """Deny Atorvastatin refill, prescribe at Express Scripts, update default pharmacy."""
    req = find_entity(state["refillRequests"], medicationName="Atorvastatin 20mg tablet", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Switching to mail-order pharmacy"

    _add_prescription(state,
                      med_name="Atorvastatin 20mg tablet",
                      sig="Take 1 tablet by mouth at bedtime",
                      qty=90, unit="tablets", refills=5, days_supply=90,
                      classification="permanent_rx",
                      pharmacy_id="pharm_011", pharmacy_name="Express Scripts Mail Pharmacy",
                      diagnosis=[{"code": "E78.5", "description": "Hyperlipidemia"}])
    state["settings"]["defaultPharmacyId"] = "pharm_011"


def solve_task_h71(state):
    """Set drug alerts to All + allergy alerts on, prescribe Cephalexin temporary."""
    state["settings"]["drugDecisionSupport"]["drugToDrugLevel"] = "all"
    state["settings"]["drugDecisionSupport"]["drugToAllergyEnabled"] = True
    _add_prescription(state,
                      med_name="Cephalexin 500mg capsule",
                      sig="Take 1 capsule by mouth three times daily",
                      qty=30, unit="capsules", refills=0, days_supply=10,
                      classification="temporary",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521")


def solve_task_h72(state):
    """Remove Penicillin allergy, discontinue Amoxicillin, prescribe Amoxicillin-Clavulanate."""
    remove_entity(state["currentPatient"]["allergies"], allergen="Penicillin")
    _discontinue_med(state, "Amoxicillin 500mg capsule", "temporaryMeds",
                     "I want to discontinue this medication",
                     details="Patient hesitant to take with allergy listed")
    _add_prescription(state,
                      med_name="Amoxicillin-Clavulanate 875mg/125mg tablet",
                      sig="Take 1 tablet by mouth twice daily for 10 days",
                      qty=20, unit="tablets", refills=0, days_supply=10,
                      classification="temporary",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "J01.90", "description": "Acute sinusitis, unspecified"}])


def solve_task_h73(state):
    """Create Gabapentin template, add PRN sig, approve Gabapentin refill."""
    tid = f"tpl_{state['_nextTplId']:03d}"
    state["_nextTplId"] += 1
    state["rxTemplates"].append({
        "id": tid,
        "medicationName": "Gabapentin 300mg capsule",
        "sig": "Take 1 capsule by mouth three times daily",
        "qty": 90,
        "unit": "capsules",
        "refills": 0,
        "daysSupply": 30,
        "ndc": None,
        "createdDate": NOW_DATE
    })

    sid = f"sig_{state['_nextSigId']:03d}"
    state["_nextSigId"] += 1
    state["customSigs"].append({
        "id": sid,
        "text": "Take 1 capsule by mouth at bedtime as needed for pain",
        "category": "prn"
    })

    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    med = find_entity(state["permanentRxMeds"], medicationName="Gabapentin 300mg capsule")
    med["lastPrescribedDate"] = NOW_DATE


def solve_task_h74(state):
    """Discontinue non-Mitchell BP meds, convert non-BP non-Mitchell meds to permanent."""
    # Losartan: Dr. Michael Chen, BP → discontinue + cancel
    _discontinue_med(state, "Losartan 50mg tablet", "permanentRxMeds",
                     "I want to discontinue this medication",
                     details="Consolidating BP management under primary provider",
                     send_cancel=True)
    # Ciprofloxacin: Dr. Lisa Park, non-BP → move to permanent Rx
    med = remove_entity(state["temporaryMeds"], medicationName="Ciprofloxacin 500mg tablet")
    med["classification"] = "permanent_rx"
    state["permanentRxMeds"].append(med)


def solve_task_h75(state):
    """Discontinue Centrum Silver, document Probiotic OTC."""
    _discontinue_med(state, "Centrum Silver Multivitamin tablet", "permanentOtcMeds",
                     "I want to discontinue this medication")
    pid = f"otc_{state['_nextOtcId']:03d}"
    state["_nextOtcId"] += 1
    state["permanentOtcMeds"].append({
        "id": pid,
        "medicationName": "Probiotic 10 Billion CFU capsule",
        "ndc": None,
        "sig": "Take 1 capsule by mouth once daily with food",
        "qty": 0,
        "unit": "capsules",
        "refills": 0,
        "refillsRemaining": 0,
        "daysSupply": 30,
        "dispenseAsWritten": False,
        "status": "active",
        "classification": "permanent_otc",
        "prescriberId": None,
        "prescriberName": None,
        "pharmacyId": None,
        "pharmacyName": None,
        "startDate": NOW_DATE,
        "lastPrescribedDate": None,
        "documentedDate": NOW_DATE,
        "diagnosis": [],
        "isControlled": False,
        "scheduleClass": None
    })


def solve_task_h76(state):
    """Approve Gabapentin (refills=5), approve Omeprazole (sig change), deny Sertraline."""
    # Gabapentin: approve with refills=5
    req = find_entity(state["refillRequests"], medicationName="Gabapentin 300mg capsule", status="pending")
    req["status"] = "approved"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["modifications"] = {"refills": 5}
    med = find_entity(state["permanentRxMeds"], medicationName="Gabapentin 300mg capsule")
    med["refillsRemaining"] = 5
    med["lastPrescribedDate"] = NOW_DATE

    # Omeprazole: approve with sig change
    req2 = find_entity(state["refillRequests"], medicationName="Omeprazole 20mg capsule", status="pending")
    req2["status"] = "approved"
    req2["processedDate"] = NOW_ISO
    req2["processedBy"] = CURRENT_USER_NAME
    req2["modifications"] = {"sig": "Take 1 capsule by mouth twice daily before meals"}
    med2 = find_entity(state["permanentRxMeds"], medicationName="Omeprazole 20mg capsule")
    med2["sig"] = "Take 1 capsule by mouth twice daily before meals"
    med2["lastPrescribedDate"] = NOW_DATE

    # Sertraline: deny
    req3 = find_entity(state["refillRequests"], medicationName="Sertraline 50mg tablet", status="pending")
    req3["status"] = "denied"
    req3["processedDate"] = NOW_ISO
    req3["processedBy"] = CURRENT_USER_NAME
    req3["denyReason"] = "Patient wants to discuss tapering at next visit"


def solve_task_h77(state):
    """Prescribe Sertraline + Losartan at Amazon Pharmacy, update default pharmacy."""
    sertraline = find_entity(state["permanentRxMeds"], medicationName="Sertraline 50mg tablet")
    _add_prescription(state,
                      med_name="Sertraline 50mg tablet",
                      sig=sertraline["sig"],
                      qty=90, unit="tablets", refills=5, days_supply=90,
                      classification="permanent_rx",
                      pharmacy_id="pharm_010", pharmacy_name="Amazon Pharmacy",
                      diagnosis=[{"code": "F41.1", "description": "Generalized anxiety disorder"}])

    losartan = find_entity(state["permanentRxMeds"], medicationName="Losartan 50mg tablet")
    _add_prescription(state,
                      med_name="Losartan 50mg tablet",
                      sig=losartan["sig"],
                      qty=90, unit="tablets", refills=5, days_supply=90,
                      classification="permanent_rx",
                      pharmacy_id="pharm_010", pharmacy_name="Amazon Pharmacy",
                      diagnosis=[{"code": "I10", "description": "Essential hypertension"}])

    state["settings"]["defaultPharmacyId"] = "pharm_010"


def solve_task_h78(state):
    """Disable settings, delete antibiotic templates."""
    state["settings"]["autoPopulateLastPharmacy"] = False
    state["settings"]["drugDecisionSupport"]["drugToDrugLevel"] = "major_only"
    state["settings"]["showCostEstimates"] = False
    remove_entity(state["rxTemplates"], medicationName="Amoxicillin 500mg capsule")
    remove_entity(state["rxTemplates"], medicationName="Azithromycin 250mg tablet (Z-Pack)")


def solve_task_h79(state):
    """Add Naproxen allergy, deny Omeprazole refill, prescribe Famotidine 20mg."""
    state["currentPatient"]["allergies"].append({
        "id": f"alg_{state['_nextAlgId']:03d}",
        "allergen": "Naproxen",
        "reaction": "GI bleeding",
        "severity": "Moderate",
        "type": "drug",
        "onsetDate": NOW_DATE,
        "source": "provider-entered"
    })
    state["_nextAlgId"] += 1

    req = find_entity(state["refillRequests"], medicationName="Omeprazole 20mg capsule", status="pending")
    req["status"] = "denied"
    req["processedDate"] = NOW_ISO
    req["processedBy"] = CURRENT_USER_NAME
    req["denyReason"] = "Patient needs GI follow-up given new allergy information"

    _add_prescription(state,
                      med_name="Famotidine 20mg tablet",
                      sig="Take 1 tablet by mouth once daily before dinner",
                      qty=30, unit="tablets", refills=3, days_supply=30,
                      classification="permanent_rx",
                      pharmacy_id="pharm_001", pharmacy_name="CVS Pharmacy #4521",
                      diagnosis=[{"code": "K21.0", "description": "Gastroesophageal reflux disease"}])


def solve_task_h80(state):
    """Discontinue Prednisone + Amoxicillin, delete their templates."""
    _discontinue_med(state, "Prednisone 10mg tablet", "temporaryMeds",
                     "I want to discontinue this medication",
                     details="Patient completed the course")
    _discontinue_med(state, "Amoxicillin 500mg capsule", "temporaryMeds",
                     "I want to discontinue this medication",
                     details="Patient completed the course")
    remove_entity(state["rxTemplates"], medicationName="Prednisone 10mg tablet (taper)")
    remove_entity(state["rxTemplates"], medicationName="Amoxicillin 500mg capsule")


# ──────────────────────────────────────────────
# Solve dispatch
# ──────────────────────────────────────────────

SOLVE_MAP = {
    "task_e1": solve_task_e1, "task_e2": solve_task_e2, "task_e3": solve_task_e3,
    "task_e4": solve_task_e4, "task_e5": solve_task_e5, "task_e6": solve_task_e6,
    "task_e7": solve_task_e7, "task_e8": solve_task_e8, "task_e9": solve_task_e9,
    "task_e10": solve_task_e10, "task_e11": solve_task_e11, "task_e12": solve_task_e12,
    "task_e13": solve_task_e13, "task_e14": solve_task_e14, "task_e15": solve_task_e15,
    "task_e16": solve_task_e16, "task_e17": solve_task_e17, "task_e18": solve_task_e18,
    "task_e19": solve_task_e19, "task_e20": solve_task_e20,

    "task_m1": solve_task_m1, "task_m2": solve_task_m2, "task_m3": solve_task_m3,
    "task_m4": solve_task_m4, "task_m5": solve_task_m5, "task_m6": solve_task_m6,
    "task_m7": solve_task_m7, "task_m8": solve_task_m8, "task_m9": solve_task_m9,
    "task_m10": solve_task_m10, "task_m11": solve_task_m11, "task_m12": solve_task_m12,
    "task_m13": solve_task_m13, "task_m14": solve_task_m14, "task_m15": solve_task_m15,
    "task_m16": solve_task_m16, "task_m17": solve_task_m17, "task_m18": solve_task_m18,
    "task_m19": solve_task_m19, "task_m20": solve_task_m20,

    "task_h1": solve_task_h1, "task_h2": solve_task_h2, "task_h3": solve_task_h3,
    "task_h4": solve_task_h4, "task_h5": solve_task_h5, "task_h6": solve_task_h6,
    "task_h7": solve_task_h7, "task_h8": solve_task_h8, "task_h9": solve_task_h9,
    "task_h10": solve_task_h10, "task_h11": solve_task_h11, "task_h12": solve_task_h12,
    "task_h13": solve_task_h13, "task_h14": solve_task_h14, "task_h15": solve_task_h15,
    "task_h16": solve_task_h16, "task_h17": solve_task_h17, "task_h18": solve_task_h18,
    "task_h19": solve_task_h19, "task_h20": solve_task_h20,

    "task_h21": solve_task_h21, "task_h22": solve_task_h22, "task_h23": solve_task_h23,
    "task_h24": solve_task_h24, "task_h25": solve_task_h25, "task_h26": solve_task_h26,
    "task_h27": solve_task_h27, "task_h28": solve_task_h28, "task_h29": solve_task_h29,
    "task_h30": solve_task_h30, "task_h31": solve_task_h31, "task_h32": solve_task_h32,
    "task_h33": solve_task_h33, "task_h34": solve_task_h34, "task_h35": solve_task_h35,
    "task_h36": solve_task_h36, "task_h37": solve_task_h37, "task_h38": solve_task_h38,
    "task_h39": solve_task_h39, "task_h40": solve_task_h40,

    "task_h41": solve_task_h41, "task_h42": solve_task_h42, "task_h43": solve_task_h43,
    "task_h44": solve_task_h44, "task_h45": solve_task_h45, "task_h46": solve_task_h46,
    "task_h47": solve_task_h47, "task_h48": solve_task_h48, "task_h49": solve_task_h49,
    "task_h50": solve_task_h50, "task_h51": solve_task_h51, "task_h52": solve_task_h52,
    "task_h53": solve_task_h53, "task_h54": solve_task_h54, "task_h55": solve_task_h55,
    "task_h56": solve_task_h56, "task_h57": solve_task_h57, "task_h58": solve_task_h58,
    "task_h59": solve_task_h59, "task_h60": solve_task_h60,

    "task_h61": solve_task_h61, "task_h62": solve_task_h62, "task_h63": solve_task_h63,
    "task_h64": solve_task_h64, "task_h65": solve_task_h65, "task_h66": solve_task_h66,
    "task_h67": solve_task_h67, "task_h68": solve_task_h68, "task_h69": solve_task_h69,
    "task_h70": solve_task_h70, "task_h71": solve_task_h71, "task_h72": solve_task_h72,
    "task_h73": solve_task_h73, "task_h74": solve_task_h74, "task_h75": solve_task_h75,
    "task_h76": solve_task_h76, "task_h77": solve_task_h77, "task_h78": solve_task_h78,
    "task_h79": solve_task_h79, "task_h80": solve_task_h80,
}


# ──────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────

def start_server(port):
    proc = subprocess.Popen(
        [sys.executable, str(APP_DIR / "server.py"), "--port", str(port)],
        cwd=str(APP_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    url = f"http://localhost:{port}"
    for _ in range(30):
        try:
            requests.get(f"{url}/api/state", timeout=1)
            return proc, url
        except Exception:
            time.sleep(0.3)
    proc.kill()
    raise RuntimeError(f"Server on port {port} failed to start")


def stop_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def run_single_task(task, seed_state, port):
    task_id = task["id"]
    solve_fn = SOLVE_MAP.get(task_id)
    if not solve_fn:
        return task_id, False, f"No solve function for {task_id}"

    proc, url = start_server(port)
    try:
        # Reset
        requests.post(f"{url}/api/reset", timeout=5)
        time.sleep(0.3)

        # Apply solve
        state = deepcopy(seed_state)
        solve_fn(state)

        # Push solved state
        resp = requests.put(f"{url}/api/state", json=state, timeout=5)
        if resp.status_code != 200:
            return task_id, False, f"Failed to push state: HTTP {resp.status_code}"

        # Verify
        verify_fn = load_verifier(task["verify"])
        passed, msg = verify_fn(url)
        return task_id, passed, msg
    except Exception as e:
        return task_id, False, f"Error: {e}"
    finally:
        stop_server(proc)


def main():
    parser = argparse.ArgumentParser(description="Sanity check for real-tasks verifiers")
    parser.add_argument("--task-id", help="Run a single task by ID")
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers")
    parser.add_argument("--port", type=int, default=9100, help="Base port")
    args = parser.parse_args()

    tasks = load_tasks()
    seed_state = get_seed_state()

    if args.task_id:
        tasks = [t for t in tasks if t["id"] == args.task_id]
        if not tasks:
            print(f"Task {args.task_id} not found")
            sys.exit(1)

    results = []
    if args.workers <= 1:
        for task in tasks:
            tid, passed, msg = run_single_task(task, seed_state, args.port)
            status = "\033[32m  PASS\033[0m" if passed else "\033[31m  FAIL\033[0m"
            print(f"{status}  {tid:12s}  {msg}")
            results.append((tid, passed, msg))
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {}
            for i, task in enumerate(tasks):
                port = args.port + i
                fut = pool.submit(run_single_task, task, seed_state, port)
                futures[fut] = task["id"]

            for fut in as_completed(futures):
                tid, passed, msg = fut.result()
                status = "\033[32m  PASS\033[0m" if passed else "\033[31m  FAIL\033[0m"
                print(f"{status}  {tid:12s}  {msg}")
                results.append((tid, passed, msg))

    passed_count = sum(1 for _, p, _ in results if p)
    total = len(results)
    print(f"\n{passed_count}/{total} passed")

    failed = [tid for tid, p, _ in results if not p]
    if failed:
        print(f"Failed: {', '.join(sorted(failed))}")
        sys.exit(1)


if __name__ == "__main__":
    main()
