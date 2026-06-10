#!/usr/bin/env python3
"""
Sanity check for Elation Clinical Records function-test tasks.

For each task, directly applies the expected end-state (bypassing the agent),
then runs the verifier and asserts it passes.

Usage:
    python3 sanity_check_function.py                     # All tasks, sequential
    python3 sanity_check_function.py --workers N          # N parallel environments
    python3 sanity_check_function.py --task-id task_5     # Single task
    python3 sanity_check_function.py --port 9000          # Custom base port
"""
import argparse
import importlib.util
import json
import os
import signal
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path

import requests

APP_DIR = Path(__file__).resolve().parent
TASKS_FILE = APP_DIR / "function-tasks.json"

# JS snippet to evaluate data.js and emit the seed state as JSON
_SEED_STATE_JS = r"""
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync(process.argv[1], 'utf8');
vm.runInThisContext(code);

const state = {
    currentProvider: JSON.parse(JSON.stringify(CURRENT_PROVIDER)),
    providers: JSON.parse(JSON.stringify(PROVIDERS)),
    patients: JSON.parse(JSON.stringify(PATIENTS)),
    problems: JSON.parse(JSON.stringify(PROBLEMS)),
    vaccinations: JSON.parse(JSON.stringify(VACCINATIONS)),
    vitals: JSON.parse(JSON.stringify(VITALS)),
    visitNotes: JSON.parse(JSON.stringify(VISIT_NOTES)),
    carePlans: JSON.parse(JSON.stringify(CARE_PLANS)),
    visitNoteCategories: JSON.parse(JSON.stringify(VISIT_NOTE_CATEGORIES)),
    visitNoteTemplates: JSON.parse(JSON.stringify(VISIT_NOTE_TEMPLATES)),
    appointmentTypes: JSON.parse(JSON.stringify(APPOINTMENT_TYPES)),
    documentTags: [...DOCUMENT_TAGS],
    providerPreferences: JSON.parse(JSON.stringify(PROVIDER_PREFERENCES)),
    _nextProblemId: 100,
    _nextVaxId: 100,
    _nextVitalId: 100,
    _nextNoteId: 100,
    _nextCarePlanId: 100,
    _nextCategoryId: 100,
    _nextTemplateId: 100,
};
process.stdout.write(JSON.stringify(state));
"""


# ── helpers ──────────────────────────────────────────────────────────

def find_patient(state, **kwargs):
    for p in state["patients"]:
        if all(p.get(k) == v for k, v in kwargs.items()):
            return p
    raise ValueError(f"Patient not found: {kwargs}")


def find_problem(state, patient_id, title):
    for p in state["problems"]:
        if p["patientId"] == patient_id and p["title"] == title:
            return p
    raise ValueError(f"Problem not found: patientId={patient_id}, title={title!r}")


def find_note(state, note_id):
    for n in state["visitNotes"]:
        if n["id"] == note_id:
            return n
    raise ValueError(f"Note not found: {note_id}")


def find_template(state, name):
    for t in state["visitNoteTemplates"]:
        if t["name"] == name:
            return t
    raise ValueError(f"Template not found: {name!r}")


def find_category(state, name):
    for c in state["visitNoteCategories"]:
        if c["name"] == name:
            return c
    raise ValueError(f"Category not found: {name!r}")


def find_appointment_type(state, name):
    for a in state["appointmentTypes"]:
        if a["name"] == name:
            return a
    raise ValueError(f"Appointment type not found: {name!r}")


# ── solve functions ──────────────────────────────────────────────────

def solve_task_1(state):
    """Add tag 'Flu-Season' to Robert Henderson."""
    patient = find_patient(state, lastName="Henderson")
    if "Flu-Season" not in patient["tags"]:
        patient["tags"].append("Flu-Season")
        patient["tags"].sort(key=lambda t: (not t.startswith("*"), t))


def solve_task_2(state):
    """Add priority tag '*High-Risk' to Emily Nakamura."""
    patient = find_patient(state, lastName="Nakamura")
    if "*High-Risk" not in patient["tags"]:
        patient["tags"].append("*High-Risk")
        patient["tags"].sort(key=lambda t: (not t.startswith("*"), t))


def solve_task_3(state):
    """Remove tag 'Smoker' from Marcus Johnson."""
    patient = find_patient(state, lastName="Johnson")
    patient["tags"] = [t for t in patient["tags"] if t != "Smoker"]


def solve_task_4(state):
    """Add tag 'New-Patient' to James Fitzgerald."""
    patient = find_patient(state, lastName="Fitzgerald")
    if "New-Patient" not in patient["tags"]:
        patient["tags"].append("New-Patient")


def solve_task_5(state):
    """Add problem 'Acute Sinusitis' (J01.90) to James Fitzgerald."""
    patient = find_patient(state, lastName="Fitzgerald")
    next_id = state.get("_nextProblemId", 100)
    existing = [p for p in state["problems"] if p["patientId"] == patient["id"]]
    problem = {
        "id": f"prob_{next_id:03d}",
        "patientId": patient["id"],
        "title": "Acute Sinusitis",
        "icd10": "J01.90",
        "icd9": "",
        "snomed": "",
        "dxDate": "2026-03-07",
        "status": "Active",
        "synopsis": "",
        "resolvedDate": "",
        "sortOrder": len(existing),
    }
    state["problems"].append(problem)
    state["_nextProblemId"] = next_id + 1


def solve_task_6(state):
    """Edit synopsis of 'Type 2 Diabetes Mellitus' for Robert Henderson."""
    patient = find_patient(state, lastName="Henderson")
    prob = find_problem(state, patient["id"], "Type 2 Diabetes Mellitus")
    prob["synopsis"] = "A1C 6.8% at last check. Well-controlled on current regimen."


def solve_task_7(state):
    """Change 'Seasonal Allergic Rhinitis' from Controlled to Active."""
    patient = find_patient(state, lastName="Henderson")
    prob = find_problem(state, patient["id"], "Seasonal Allergic Rhinitis")
    prob["status"] = "Active"
    prob["resolvedDate"] = ""


def solve_task_8(state):
    """Change 'Generalized Anxiety Disorder' for Nakamura to Resolved."""
    patient = find_patient(state, lastName="Nakamura")
    prob = find_problem(state, patient["id"], "Generalized Anxiety Disorder")
    prob["status"] = "Resolved"
    prob["resolvedDate"] = "2026-03-07"


def solve_task_9(state):
    """Change 'Plantar Fasciitis, Right Foot' for Nakamura to Active."""
    patient = find_patient(state, lastName="Nakamura")
    prob = find_problem(state, patient["id"], "Plantar Fasciitis, Right Foot")
    prob["status"] = "Active"
    prob["resolvedDate"] = ""


def solve_task_10(state):
    """Edit onset date of 'Essential Hypertension, Uncontrolled' for Johnson."""
    patient = find_patient(state, lastName="Johnson")
    prob = find_problem(state, patient["id"], "Essential Hypertension, Uncontrolled")
    prob["dxDate"] = "2015-01-10"


def solve_task_11(state):
    """Add problem 'Insomnia' (G47.00) Controlled to Sofia Rodriguez-Martinez."""
    patient = find_patient(state, lastName="Rodriguez-Martinez")
    next_id = state.get("_nextProblemId", 100)
    existing = [p for p in state["problems"] if p["patientId"] == patient["id"]]
    problem = {
        "id": f"prob_{next_id:03d}",
        "patientId": patient["id"],
        "title": "Insomnia",
        "icd10": "G47.00",
        "icd9": "",
        "snomed": "",
        "dxDate": "2026-03-07",
        "status": "Controlled",
        "synopsis": "",
        "resolvedDate": "",
        "sortOrder": len(existing),
    }
    state["problems"].append(problem)
    state["_nextProblemId"] = next_id + 1


def solve_task_12(state):
    """Edit title of 'Chronic Low Back Pain' for Johnson."""
    patient = find_patient(state, lastName="Johnson")
    prob = find_problem(state, patient["id"], "Chronic Low Back Pain")
    prob["title"] = "Chronic Low Back Pain with Lumbar Disc Degeneration"


def solve_task_13(state):
    """Add problem 'Urinary Tract Infection' (N39.0) to Priya Sharma."""
    patient = find_patient(state, lastName="Sharma")
    next_id = state.get("_nextProblemId", 100)
    existing = [p for p in state["problems"] if p["patientId"] == patient["id"]]
    problem = {
        "id": f"prob_{next_id:03d}",
        "patientId": patient["id"],
        "title": "Urinary Tract Infection",
        "icd10": "N39.0",
        "icd9": "",
        "snomed": "",
        "dxDate": "2026-03-07",
        "status": "Active",
        "synopsis": "",
        "resolvedDate": "",
        "sortOrder": len(existing),
    }
    state["problems"].append(problem)
    state["_nextProblemId"] = next_id + 1


def solve_task_14(state):
    """Change 'Hypothyroidism' for Helen Zhao to Resolved."""
    patient = find_patient(state, lastName="Zhao")
    prob = find_problem(state, patient["id"], "Hypothyroidism")
    prob["status"] = "Resolved"
    prob["resolvedDate"] = "2026-03-07"


def solve_task_15(state):
    """Add Influenza vaccine for Emily Nakamura."""
    patient = find_patient(state, lastName="Nakamura")
    next_id = state.get("_nextVaxId", 100)
    vax = {
        "id": f"vax_{next_id:03d}",
        "patientId": patient["id"],
        "vaccineName": "Influenza (IIV4) Preservative Free",
        "cvx": "185",
        "ndc": "",
        "manufacturer": "Sanofi Pasteur",
        "lotNumber": "",
        "expirationDate": "",
        "doseAmount": "",
        "doseUnits": "",
        "seriesNumber": "",
        "method": "Intramuscular",
        "site": "Left Deltoid",
        "givenOn": "2026-03-07T10:00:00Z",
        "orderedBy": state["currentProvider"]["id"],
        "givenBy": state["currentProvider"]["id"],
        "recordType": "New",
        "visDate": "",
        "recall": "",
        "reason": "",
        "notes": "",
        "program": "Not VFC Eligible",
        "fundedBy": "Private",
        "source": "New Immunization",
        "status": "completed",
    }
    state["vaccinations"].append(vax)
    state["_nextVaxId"] = next_id + 1


def solve_task_16(state):
    """Add historical Hepatitis B record for James Fitzgerald."""
    patient = find_patient(state, lastName="Fitzgerald")
    next_id = state.get("_nextVaxId", 100)
    vax = {
        "id": f"vax_{next_id:03d}",
        "patientId": patient["id"],
        "vaccineName": "Hepatitis B (Engerix-B)",
        "cvx": "",
        "ndc": "",
        "manufacturer": "",
        "lotNumber": "",
        "expirationDate": "",
        "doseAmount": "",
        "doseUnits": "",
        "seriesNumber": "",
        "method": "",
        "site": "",
        "givenOn": "2026-03-07T00:00:00Z",
        "orderedBy": "",
        "givenBy": "",
        "recordType": "Historical",
        "visDate": "",
        "recall": "",
        "reason": "",
        "notes": "",
        "program": "",
        "fundedBy": "",
        "source": "Historical",
        "status": "completed",
    }
    state["vaccinations"].append(vax)
    state["_nextVaxId"] = next_id + 1


def solve_task_17(state):
    """Add declined Influenza record for David Kowalski."""
    patient = find_patient(state, lastName="Kowalski")
    next_id = state.get("_nextVaxId", 100)
    vax = {
        "id": f"vax_{next_id:03d}",
        "patientId": patient["id"],
        "vaccineName": "Influenza (IIV4) Standard",
        "cvx": "",
        "ndc": "",
        "manufacturer": "",
        "lotNumber": "",
        "expirationDate": "",
        "doseAmount": "",
        "doseUnits": "",
        "seriesNumber": "",
        "method": "",
        "site": "",
        "givenOn": "2026-03-07T00:00:00Z",
        "orderedBy": state["currentProvider"]["id"],
        "givenBy": "",
        "recordType": "Declined",
        "visDate": "",
        "recall": "",
        "reason": "Patient prefers not to vaccinate this season",
        "notes": "",
        "program": "",
        "fundedBy": "",
        "source": "",
        "status": "declined",
    }
    state["vaccinations"].append(vax)
    state["_nextVaxId"] = next_id + 1


def solve_task_18(state):
    """Add Tdap for Sofia Rodriguez-Martinez."""
    patient = find_patient(state, lastName="Rodriguez-Martinez")
    next_id = state.get("_nextVaxId", 100)
    vax = {
        "id": f"vax_{next_id:03d}",
        "patientId": patient["id"],
        "vaccineName": "Tdap (Adacel)",
        "cvx": "115",
        "ndc": "",
        "manufacturer": "",
        "lotNumber": "TDP-5590",
        "expirationDate": "2027-06-30",
        "doseAmount": "",
        "doseUnits": "",
        "seriesNumber": "",
        "method": "",
        "site": "",
        "givenOn": "2026-03-07T10:00:00Z",
        "orderedBy": state["currentProvider"]["id"],
        "givenBy": state["currentProvider"]["id"],
        "recordType": "New",
        "visDate": "",
        "recall": "",
        "reason": "",
        "notes": "",
        "program": "Not VFC Eligible",
        "fundedBy": "Private",
        "source": "New Immunization",
        "status": "completed",
    }
    state["vaccinations"].append(vax)
    state["_nextVaxId"] = next_id + 1


def solve_task_19(state):
    """Add Ketorolac injectable for Marcus Johnson."""
    patient = find_patient(state, lastName="Johnson")
    next_id = state.get("_nextVaxId", 100)
    vax = {
        "id": f"vax_{next_id:03d}",
        "patientId": patient["id"],
        "vaccineName": "Ketorolac (Toradol)",
        "cvx": "",
        "ndc": "",
        "manufacturer": "",
        "lotNumber": "",
        "expirationDate": "",
        "doseAmount": "",
        "doseUnits": "",
        "seriesNumber": "",
        "method": "Intramuscular",
        "site": "Left Gluteal",
        "givenOn": "2026-03-07T10:00:00Z",
        "orderedBy": state["currentProvider"]["id"],
        "givenBy": state["currentProvider"]["id"],
        "recordType": "New",
        "visDate": "",
        "recall": "",
        "reason": "",
        "notes": "",
        "program": "",
        "fundedBy": "Private",
        "source": "New Immunization",
        "status": "completed",
        "isInjectable": True,
        "notSendToRegistry": True,
    }
    state["vaccinations"].append(vax)
    state["_nextVaxId"] = next_id + 1


def solve_task_20(state):
    """Add DTaP for Aaliyah Washington with VFC."""
    patient = find_patient(state, lastName="Washington")
    next_id = state.get("_nextVaxId", 100)
    vax = {
        "id": f"vax_{next_id:03d}",
        "patientId": patient["id"],
        "vaccineName": "DTaP (Daptacel)",
        "cvx": "20",
        "ndc": "",
        "manufacturer": "",
        "lotNumber": "",
        "expirationDate": "",
        "doseAmount": "",
        "doseUnits": "",
        "seriesNumber": "",
        "method": "",
        "site": "",
        "givenOn": "2026-03-07T10:00:00Z",
        "orderedBy": state["currentProvider"]["id"],
        "givenBy": state["currentProvider"]["id"],
        "recordType": "New",
        "visDate": "",
        "recall": "",
        "reason": "",
        "notes": "",
        "program": "VFC Eligible",
        "fundedBy": "VFC",
        "source": "New Immunization",
        "status": "completed",
    }
    state["vaccinations"].append(vax)
    state["_nextVaxId"] = next_id + 1


def solve_task_21(state):
    """Add COVID-19 Moderna for Thomas Bergstrom."""
    patient = find_patient(state, lastName="Bergstrom")
    next_id = state.get("_nextVaxId", 100)
    vax = {
        "id": f"vax_{next_id:03d}",
        "patientId": patient["id"],
        "vaccineName": "COVID-19 Moderna",
        "cvx": "207",
        "ndc": "",
        "manufacturer": "Moderna",
        "lotNumber": "",
        "expirationDate": "",
        "doseAmount": "",
        "doseUnits": "",
        "seriesNumber": "",
        "method": "",
        "site": "",
        "givenOn": "2026-03-07T10:00:00Z",
        "orderedBy": state["currentProvider"]["id"],
        "givenBy": state["currentProvider"]["id"],
        "recordType": "New",
        "visDate": "",
        "recall": "3 weeks",
        "reason": "",
        "notes": "",
        "program": "Not VFC Eligible",
        "fundedBy": "Private",
        "source": "New Immunization",
        "status": "completed",
    }
    state["vaccinations"].append(vax)
    state["_nextVaxId"] = next_id + 1


def solve_task_22(state):
    """Add vitals for Emily Nakamura: BP 120/74, HR 70, RR 16."""
    patient = find_patient(state, lastName="Nakamura")
    next_id = state.get("_nextVitalId", 100)
    vital = {
        "id": f"vit_{next_id:03d}",
        "patientId": patient["id"],
        "noteId": "",
        "date": "2026-03-07T10:00:00Z",
        "bloodPressureSystolic": 120,
        "bloodPressureDiastolic": 74,
        "heartRate": 70,
        "respiratoryRate": 16,
        "temperature": None,
        "temperatureUnit": "F",
        "oxygenSaturation": None,
        "weight": None,
        "weightUnit": "lbs",
        "height": None,
        "heightUnit": "in",
        "bmi": None,
        "painLevel": None,
    }
    state["vitals"].append(vital)
    state["_nextVitalId"] = next_id + 1


def solve_task_23(state):
    """Add vitals for Marcus Johnson: temp 37.2 C."""
    patient = find_patient(state, lastName="Johnson")
    next_id = state.get("_nextVitalId", 100)
    vital = {
        "id": f"vit_{next_id:03d}",
        "patientId": patient["id"],
        "noteId": "",
        "date": "2026-03-07T10:00:00Z",
        "bloodPressureSystolic": None,
        "bloodPressureDiastolic": None,
        "heartRate": None,
        "respiratoryRate": None,
        "temperature": 37.2,
        "temperatureUnit": "C",
        "oxygenSaturation": None,
        "weight": None,
        "weightUnit": "lbs",
        "height": None,
        "heightUnit": "in",
        "bmi": None,
        "painLevel": None,
    }
    state["vitals"].append(vital)
    state["_nextVitalId"] = next_id + 1


def solve_task_24(state):
    """Add vitals for Helen Zhao: weight 58 kg, height 157 cm."""
    patient = find_patient(state, lastName="Zhao")
    next_id = state.get("_nextVitalId", 100)
    vital = {
        "id": f"vit_{next_id:03d}",
        "patientId": patient["id"],
        "noteId": "",
        "date": "2026-03-07T10:00:00Z",
        "bloodPressureSystolic": None,
        "bloodPressureDiastolic": None,
        "heartRate": None,
        "respiratoryRate": None,
        "temperature": None,
        "temperatureUnit": "F",
        "oxygenSaturation": None,
        "weight": 58,
        "weightUnit": "kg",
        "height": 157,
        "heightUnit": "cm",
        "bmi": None,
        "painLevel": None,
    }
    state["vitals"].append(vital)
    state["_nextVitalId"] = next_id + 1


def solve_task_25(state):
    """Add vitals for David Kowalski: pain level 6."""
    patient = find_patient(state, lastName="Kowalski")
    next_id = state.get("_nextVitalId", 100)
    vital = {
        "id": f"vit_{next_id:03d}",
        "patientId": patient["id"],
        "noteId": "",
        "date": "2026-03-07T10:00:00Z",
        "bloodPressureSystolic": None,
        "bloodPressureDiastolic": None,
        "heartRate": None,
        "respiratoryRate": None,
        "temperature": None,
        "temperatureUnit": "F",
        "oxygenSaturation": None,
        "weight": None,
        "weightUnit": "lbs",
        "height": None,
        "heightUnit": "in",
        "bmi": None,
        "painLevel": 6,
    }
    state["vitals"].append(vital)
    state["_nextVitalId"] = next_id + 1


def solve_task_26(state):
    """Add vitals for Sofia Rodriguez-Martinez: SpO2 98, BP 110/68."""
    patient = find_patient(state, lastName="Rodriguez-Martinez")
    next_id = state.get("_nextVitalId", 100)
    vital = {
        "id": f"vit_{next_id:03d}",
        "patientId": patient["id"],
        "noteId": "",
        "date": "2026-03-07T10:00:00Z",
        "bloodPressureSystolic": 110,
        "bloodPressureDiastolic": 68,
        "heartRate": None,
        "respiratoryRate": None,
        "temperature": None,
        "temperatureUnit": "F",
        "oxygenSaturation": 98,
        "weight": None,
        "weightUnit": "lbs",
        "height": None,
        "heightUnit": "in",
        "bmi": None,
        "painLevel": None,
    }
    state["vitals"].append(vital)
    state["_nextVitalId"] = next_id + 1


def solve_task_27(state):
    """Create draft note for James Fitzgerald with reason 'New Patient Visit'."""
    patient = find_patient(state, lastName="Fitzgerald")
    next_id = state.get("_nextNoteId", 100)
    note = {
        "id": f"note_{next_id:03d}",
        "patientId": patient["id"],
        "providerId": state["currentProvider"]["id"],
        "format": state["currentProvider"]["defaultNoteFormat"],
        "category": state["currentProvider"]["defaultCategory"],
        "templateUsed": "",
        "date": "2026-03-07T10:00:00Z",
        "status": "draft",
        "signedAt": "",
        "reason": "New Patient Visit",
        "blocks": [],
        "billingItems": [],
        "documentTags": [],
    }
    state["visitNotes"].append(note)
    state["_nextNoteId"] = next_id + 1


def solve_task_28(state):
    """Create note with Simple Note format for Priya Sharma."""
    patient = find_patient(state, lastName="Sharma")
    next_id = state.get("_nextNoteId", 100)
    note = {
        "id": f"note_{next_id:03d}",
        "patientId": patient["id"],
        "providerId": state["currentProvider"]["id"],
        "format": "simple",
        "category": state["currentProvider"]["defaultCategory"],
        "templateUsed": "",
        "date": "2026-03-07T10:00:00Z",
        "status": "draft",
        "signedAt": "",
        "reason": "",
        "blocks": [],
        "billingItems": [],
        "documentTags": [],
    }
    state["visitNotes"].append(note)
    state["_nextNoteId"] = next_id + 1


def solve_task_29(state):
    """Create note with Telehealth category for Thomas Bergstrom."""
    patient = find_patient(state, lastName="Bergstrom")
    next_id = state.get("_nextNoteId", 100)
    note = {
        "id": f"note_{next_id:03d}",
        "patientId": patient["id"],
        "providerId": state["currentProvider"]["id"],
        "format": state["currentProvider"]["defaultNoteFormat"],
        "category": "cat_002",
        "templateUsed": "",
        "date": "2026-03-07T10:00:00Z",
        "status": "draft",
        "signedAt": "",
        "reason": "",
        "blocks": [],
        "billingItems": [],
        "documentTags": [],
    }
    state["visitNotes"].append(note)
    state["_nextNoteId"] = next_id + 1


def solve_task_30(state):
    """Create note using Diabetes Management template for Robert Henderson."""
    patient = find_patient(state, lastName="Henderson")
    tmpl = find_template(state, "Diabetes Management")
    next_id = state.get("_nextNoteId", 100)
    # Build blocks from template content
    blocks = []
    for section in ["hpi", "ros", "pe", "assessment"]:
        if tmpl.get("content", {}).get(section):
            blocks.append({"type": section, "content": tmpl["content"][section]})
    note = {
        "id": f"note_{next_id:03d}",
        "patientId": patient["id"],
        "providerId": state["currentProvider"]["id"],
        "format": state["currentProvider"]["defaultNoteFormat"],
        "category": state["currentProvider"]["defaultCategory"],
        "templateUsed": tmpl["id"],
        "date": "2026-03-07T10:00:00Z",
        "status": "draft",
        "signedAt": "",
        "reason": "",
        "blocks": blocks,
        "billingItems": deepcopy(tmpl.get("billingItems", [])),
        "documentTags": list(tmpl.get("documentTags", [])),
    }
    state["visitNotes"].append(note)
    state["_nextNoteId"] = next_id + 1


def solve_task_31(state):
    """Sign draft note_012."""
    note = find_note(state, "note_012")
    note["status"] = "signed"
    note["signedAt"] = "2026-03-07T10:00:00Z"


def solve_task_32(state):
    """Add PE block to note_012."""
    note = find_note(state, "note_012")
    note["blocks"].append({
        "type": "pe",
        "content": "General: Alert, oriented. Lumbar spine tenderness to palpation.",
    })


def solve_task_33(state):
    """Edit HPI block content in note_012."""
    note = find_note(state, "note_012")
    for block in note["blocks"]:
        if block["type"] == "hpi":
            block["content"] = (
                "Patient returns for 6-week follow-up. Reports improvement in "
                "back pain with physical therapy. Anxiety well-managed on current medication."
            )
            return
    raise ValueError("HPI block not found in note_012")


def solve_task_34(state):
    """Remove HPI block from note_012."""
    note = find_note(state, "note_012")
    note["blocks"] = [b for b in note["blocks"] if b["type"] != "hpi"]


def solve_task_35(state):
    """Add billing item CPT 99213 to note_012."""
    note = find_note(state, "note_012")
    note["billingItems"].append({
        "cptCode": "99213",
        "description": "Office visit, established, low complexity",
    })


def solve_task_36(state):
    """Create template 'Chronic Pain Follow-Up'."""
    next_id = state.get("_nextTemplateId", 100)
    tmpl = {
        "id": f"tmpl_{next_id:03d}",
        "name": "Chronic Pain Follow-Up",
        "createdBy": state["currentProvider"]["id"],
        "content": {
            "hpi": "Patient presents for chronic pain management follow-up.",
        },
        "billingItems": [],
        "pos": "",
        "billingNotes": "",
        "documentTags": [],
        "createdAt": "2026-03-07T10:00:00Z",
    }
    state["visitNoteTemplates"].append(tmpl)
    state["_nextTemplateId"] = next_id + 1


def solve_task_37(state):
    """Rename 'Telehealth Follow-Up' to 'Virtual Visit Follow-Up'."""
    tmpl = find_template(state, "Telehealth Follow-Up")
    tmpl["name"] = "Virtual Visit Follow-Up"


def solve_task_38(state):
    """Duplicate template 'E* Annual Wellness Visit'."""
    orig = find_template(state, "E* Annual Wellness Visit")
    next_id = state.get("_nextTemplateId", 100)
    copy = deepcopy(orig)
    copy["id"] = f"tmpl_{next_id:03d}"
    copy["name"] = orig["name"] + " (Copy)"
    copy["createdAt"] = "2026-03-07T10:00:00Z"
    state["visitNoteTemplates"].append(copy)
    state["_nextTemplateId"] = next_id + 1


def solve_task_39(state):
    """Delete template 'Injectable Administration'."""
    state["visitNoteTemplates"] = [
        t for t in state["visitNoteTemplates"]
        if t["name"] != "Injectable Administration"
    ]


def solve_task_40(state):
    """Edit billing notes of 'Pre-Operative Evaluation'."""
    tmpl = find_template(state, "Pre-Operative Evaluation")
    tmpl["billingNotes"] = (
        "Pre-op clearance - ensure all required labs are completed prior to surgery."
    )


def solve_task_41(state):
    """Add document tag 'Chronic-Pain' to template 'Diabetes Management'."""
    tmpl = find_template(state, "Diabetes Management")
    if "Chronic-Pain" not in tmpl["documentTags"]:
        tmpl["documentTags"].append("Chronic-Pain")


def solve_task_42(state):
    """Edit HPI content of 'Hypertension Follow-Up'."""
    tmpl = find_template(state, "Hypertension Follow-Up")
    tmpl["content"]["hpi"] = (
        "Patient returns for blood pressure management follow-up. "
        "Reviewing home BP log and medication compliance."
    )


def solve_task_43(state):
    """Add category 'Behavioral Health' with MIPS enabled."""
    next_id = state.get("_nextCategoryId", 100)
    max_sort = max(c["sortOrder"] for c in state["visitNoteCategories"])
    cat = {
        "id": f"cat_{next_id:03d}",
        "name": "Behavioral Health",
        "countForMIPS": True,
        "isDefault": False,
        "sortOrder": max_sort + 1,
    }
    state["visitNoteCategories"].append(cat)
    state["_nextCategoryId"] = next_id + 1


def solve_task_44(state):
    """Rename 'Workers Comp' to 'Workers Compensation'."""
    cat = find_category(state, "Workers Comp")
    cat["name"] = "Workers Compensation"


def solve_task_45(state):
    """Remove category 'Care Plan Review'."""
    state["visitNoteCategories"] = [
        c for c in state["visitNoteCategories"]
        if c["name"] != "Care Plan Review"
    ]


def solve_task_46(state):
    """Toggle MIPS off on 'Procedure'."""
    cat = find_category(state, "Procedure")
    cat["countForMIPS"] = False


def solve_task_47(state):
    """Toggle MIPS on on 'Vaccination Only'."""
    cat = find_category(state, "Vaccination Only")
    cat["countForMIPS"] = True


def solve_task_48(state):
    """Disable coded assessments."""
    state["providerPreferences"]["codedAssessments"] = False


def solve_task_49(state):
    """Enable show Dx codes in print."""
    state["providerPreferences"]["showDxCodesInPrint"] = True


def solve_task_50(state):
    """Change default note format to simple."""
    state["providerPreferences"]["defaultNoteFormat"] = "simple"


def solve_task_51(state):
    """Change 'Office Visit' appointment format to hp_single."""
    apt = find_appointment_type(state, "Office Visit")
    apt["noteFormat"] = "hp_single"


def solve_task_52(state):
    """Change 'Telehealth Visit' category to Follow-Up (cat_005)."""
    apt = find_appointment_type(state, "Telehealth Visit")
    apt["noteCategory"] = "cat_005"


def solve_task_53(state):
    """Change 'Follow-Up' template to Hypertension Follow-Up (tmpl_007)."""
    apt = find_appointment_type(state, "Follow-Up")
    apt["noteTemplate"] = "tmpl_007"


def solve_task_54(state):
    """Set 'Urgent Same-Day' template to E* Problem-Focused Visit (tmpl_002)."""
    apt = find_appointment_type(state, "Urgent Same-Day")
    apt["noteTemplate"] = "tmpl_002"


def solve_task_55(state):
    """Change 'COVID Vaccine' format to non_visit."""
    apt = find_appointment_type(state, "COVID Vaccine")
    apt["noteFormat"] = "non_visit"


SOLVERS = {
    f"task_{i}": globals()[f"solve_task_{i}"]
    for i in range(1, 56)
}


# ── server management ────────────────────────────────────────────────

def generate_seed_state():
    """Use Node.js to evaluate data.js and produce the seed state JSON."""
    data_js = str(APP_DIR / "js" / "data.js")
    result = subprocess.run(
        ["node", "-e", _SEED_STATE_JS, data_js],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate seed state:\n{result.stderr}")
    return json.loads(result.stdout)


def seed_server(server_url, seed_state):
    """PUT the seed state to the server to establish the baseline."""
    resp = requests.put(
        f"{server_url}/api/state",
        json=seed_state,
        headers={"Content-Type": "application/json"},
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to seed server: HTTP {resp.status_code}")


def find_free_port(start=9000):
    """Find a free port starting from `start`."""
    port = start
    while port < start + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"No free port found in range {start}-{start+100}")


def start_server(port):
    """Start the server on the given port."""
    proc = subprocess.Popen(
        [sys.executable, "server.py", "--port", str(port)],
        cwd=str(APP_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(30):
        try:
            requests.get(f"http://localhost:{port}/", timeout=1)
            return proc
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(0.2)
    proc.kill()
    raise RuntimeError(f"Server failed to start on port {port}")


def stop_server(proc):
    """Stop the server process."""
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ── task runner ──────────────────────────────────────────────────────

def load_tasks():
    """Load task definitions from function-tasks.json."""
    with open(TASKS_FILE) as f:
        return json.load(f)


def load_verifier(verify_path):
    """Dynamically load a verifier module."""
    full_path = APP_DIR / verify_path
    spec = importlib.util.spec_from_file_location("verifier", str(full_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


def run_single_task(task, server_url):
    """Reset -> solve -> verify for a single task."""
    task_id = task["id"]
    solver = SOLVERS.get(task_id)
    if not solver:
        return task_id, False, f"No solver defined for {task_id}"

    try:
        # 1. Reset to seed state
        resp = requests.post(f"{server_url}/api/reset")
        if resp.status_code != 200:
            return task_id, False, f"Reset failed: HTTP {resp.status_code}"

        time.sleep(0.3)

        # 2. Read seed state
        resp = requests.get(f"{server_url}/api/state")
        if resp.status_code != 200:
            return task_id, False, f"Could not read state after reset: HTTP {resp.status_code}"
        state = resp.json()

        # 3. Apply the solve function
        solver(state)

        # 4. Write solved state back
        resp = requests.put(
            f"{server_url}/api/state",
            json=state,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            return task_id, False, f"Could not write state: HTTP {resp.status_code}"

        # 5. Run the verifier
        verify_fn = load_verifier(task["verify"])
        passed, message = verify_fn(server_url)
        return task_id, passed, message

    except Exception as e:
        return task_id, False, f"Exception: {e}"


def run_tasks_sequential(tasks, port, seed_state):
    """Run all tasks sequentially on a single server."""
    proc = start_server(port)
    server_url = f"http://localhost:{port}"
    results = []
    try:
        seed_server(server_url, seed_state)
        for task in tasks:
            result = run_single_task(task, server_url)
            results.append(result)
            status = "\033[32m  PASS\033[0m" if result[1] else "\033[31m  FAIL\033[0m"
            print(f"{status}  {result[0]:12s}  {result[2]}")
    finally:
        stop_server(proc)
    return results


def run_tasks_parallel(tasks, workers, base_port, seed_state):
    """Run tasks in parallel across multiple server instances."""
    results = []

    def worker_fn(task, port):
        proc = start_server(port)
        server_url = f"http://localhost:{port}"
        try:
            seed_server(server_url, seed_state)
            return run_single_task(task, server_url)
        finally:
            stop_server(proc)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}
        for i, task in enumerate(tasks):
            port = base_port + i
            future = executor.submit(worker_fn, task, port)
            futures[future] = task["id"]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "\033[32m  PASS\033[0m" if result[1] else "\033[31m  FAIL\033[0m"
            print(f"{status}  {result[0]:12s}  {result[2]}")

    return results


# ── main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Elation Clinical Records function-task sanity check"
    )
    parser.add_argument("--task-id", type=str, help="Run a single task by ID")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--port", type=int, default=9500, help="Base port for servers")
    args = parser.parse_args()

    tasks = load_tasks()
    if args.task_id:
        tasks = [t for t in tasks if t["id"] == args.task_id]
        if not tasks:
            print(f"Task '{args.task_id}' not found.")
            sys.exit(1)

    print("Generating seed state from JS data...")
    seed_state = generate_seed_state()
    print(f"Running {len(tasks)} task(s)...\n")

    if args.workers <= 1:
        port = find_free_port(args.port)
        results = run_tasks_sequential(tasks, port, seed_state)
    else:
        results = run_tasks_parallel(tasks, args.workers, args.port, seed_state)

    # Summary
    passed = sum(1 for _, p, _ in results if p)
    total = len(results)
    failed = [tid for tid, p, _ in results if not p]

    print(f"\n{passed}/{total} passed")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
