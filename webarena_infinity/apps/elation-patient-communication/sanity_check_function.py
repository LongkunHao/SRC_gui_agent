#!/usr/bin/env python3
"""
Sanity check for Elation Patient Communication function-test tasks.

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
_SEED_STATE_JS = """
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync(process.argv[1], 'utf8');
vm.runInThisContext(code);

// Replicate what AppState._loadSeedData() does
const state = {
    _seedVersion: SEED_DATA_VERSION,
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    providers: JSON.parse(JSON.stringify(PROVIDERS)),
    userGroups: JSON.parse(JSON.stringify(USER_GROUPS)),
    patients: JSON.parse(JSON.stringify(PATIENTS)),
    patientLetters: JSON.parse(JSON.stringify(PATIENT_LETTERS)),
    appointments: JSON.parse(JSON.stringify(APPOINTMENTS)),
    reminders: JSON.parse(JSON.stringify(REMINDERS)),
    bulkLetters: JSON.parse(JSON.stringify(BULK_LETTERS)),
    visitSummaries: JSON.parse(JSON.stringify(VISIT_SUMMARIES)),
    practiceSettings: JSON.parse(JSON.stringify(PRACTICE_SETTINGS)),
    messageRouting: JSON.parse(JSON.stringify(MESSAGE_ROUTING)),
    messageCategories: [...MESSAGE_CATEGORIES],
    patientTags: [...PATIENT_TAGS],
    sharingLevels: JSON.parse(JSON.stringify(SHARING_LEVELS)),
    notificationTimeframes: JSON.parse(JSON.stringify(NOTIFICATION_TIMEFRAMES)),
    _nextPatientId: INITIAL_COUNTERS._nextPatientId,
    _nextLetterId: INITIAL_COUNTERS._nextLetterId,
    _nextConversationId: INITIAL_COUNTERS._nextConversationId,
    _nextAppointmentId: INITIAL_COUNTERS._nextAppointmentId,
    _nextReminderId: INITIAL_COUNTERS._nextReminderId,
    _nextBulkLetterId: INITIAL_COUNTERS._nextBulkLetterId,
    _nextVisitSummaryId: INITIAL_COUNTERS._nextVisitSummaryId,
    _nextLocationId: INITIAL_COUNTERS._nextLocationId,
    _nextCptCodeId: INITIAL_COUNTERS._nextCptCodeId,
};
process.stdout.write(JSON.stringify(state));
"""


# ── helpers ──────────────────────────────────────────────────────────

def find_entity(entities, **kwargs):
    """Find an entity by attribute match. Raises if not found."""
    for e in entities:
        if all(e.get(k) == v for k, v in kwargs.items()):
            return e
    raise ValueError(f"Entity not found: {kwargs}")


def find_patient_by_name(state, first, last):
    """Find a patient by first and last name."""
    return find_entity(state["patients"], firstName=first, lastName=last)


def find_provider(state, provider_id):
    """Find a provider by ID."""
    return find_entity(state["providers"], id=provider_id)


def find_letter(state, letter_id):
    """Find a letter by ID."""
    return find_entity(state["patientLetters"], id=letter_id)


def find_reminder(state, reminder_id):
    """Find a reminder by ID."""
    return find_entity(state["reminders"], id=reminder_id)


def find_appointment_by_patient_reason(state, patient_id, reason_fragment):
    """Find an appointment by patient ID and reason fragment."""
    for a in state["appointments"]:
        if a["patientId"] == patient_id and reason_fragment.lower() in a.get("reason", "").lower():
            return a
    raise ValueError(f"Appointment not found: patient={patient_id}, reason containing '{reason_fragment}'")


def find_location_by_name(state, name):
    """Find a practice location by name."""
    for loc in state["practiceSettings"]["practiceLocations"]:
        if loc["name"] == name:
            return loc
    raise ValueError(f"Location not found: {name!r}")


def next_letter_id(state):
    """Get and increment the next letter ID."""
    lid = state["_nextLetterId"]
    state["_nextLetterId"] = lid + 1
    return f"ltr_{lid}"


def next_conversation_id(state):
    """Get and increment the next conversation ID."""
    cid = state["_nextConversationId"]
    state["_nextConversationId"] = cid + 1
    return f"conv_{cid}"


def next_appointment_id(state):
    """Get and increment the next appointment ID."""
    aid = state["_nextAppointmentId"]
    state["_nextAppointmentId"] = aid + 1
    return f"appt_{aid}"


def next_bulk_letter_id(state):
    """Get and increment the next bulk letter ID."""
    bid = state["_nextBulkLetterId"]
    state["_nextBulkLetterId"] = bid + 1
    return f"bulk_{bid}"


def next_location_id(state):
    """Get and increment the next location ID."""
    lid = state["_nextLocationId"]
    state["_nextLocationId"] = lid + 1
    return f"loc_{lid}"


TIMESTAMP = "2026-03-02T12:00:00Z"


# ── solve functions ──────────────────────────────────────────────────

def solve_task_1(state):
    """Mark Emily Thompson's unread message as read."""
    letter = find_letter(state, "ltr_4")
    letter["isRead"] = True
    letter["readAt"] = TIMESTAMP


def solve_task_2(state):
    """Mark Sophia Nguyen's appointment request as read."""
    letter = find_letter(state, "ltr_6")
    letter["isRead"] = True
    letter["readAt"] = TIMESTAMP


def solve_task_3(state):
    """Reply to James Rodriguez's prescription refill conversation."""
    state["patientLetters"].append({
        "id": next_letter_id(state),
        "patientId": "pat_1",
        "conversationId": "conv_1",
        "direction": "to_patient",
        "subject": "Re: Prescription Refill",
        "body": "Yes, I will also send a refill for your Lisinopril. You can pick both up at your pharmacy tomorrow.",
        "category": None,
        "senderId": "prov_1",
        "senderType": "provider",
        "attachments": [],
        "postDate": None,
        "sentAt": TIMESTAMP,
        "readAt": None,
        "isRead": False,
        "isDraft": False,
        "conversationState": "open",
        "doNotAllowResponse": False,
        "unreadAlertTimeframe": "none",
        "printHeader": "default"
    })


def solve_task_4(state):
    """Reply to Howard Blackwell's gardening question."""
    state["patientLetters"].append({
        "id": next_letter_id(state),
        "patientId": "pat_27",
        "conversationId": "conv_24",
        "direction": "to_patient",
        "subject": "Re: General Question",
        "body": "Light gardening should be fine this spring. Start slowly and avoid heavy lifting. Stop if you feel short of breath.",
        "category": None,
        "senderId": "prov_1",
        "senderType": "provider",
        "attachments": [],
        "postDate": None,
        "sentAt": TIMESTAMP,
        "readAt": None,
        "isRead": False,
        "isDraft": False,
        "conversationState": "open",
        "doNotAllowResponse": False,
        "unreadAlertTimeframe": "none",
        "printHeader": "default"
    })


def solve_task_5(state):
    """End conversation conv_9 (Maria Gonzalez lab results)."""
    for letter in state["patientLetters"]:
        if letter["conversationId"] == "conv_9":
            letter["conversationState"] = "ended"


def solve_task_6(state):
    """End conversation conv_22 (Aisha Patel prenatal)."""
    for letter in state["patientLetters"]:
        if letter["conversationId"] == "conv_22":
            letter["conversationState"] = "ended"


def solve_task_7(state):
    """Send new letter to David Park."""
    conv_id = next_conversation_id(state)
    state["patientLetters"].append({
        "id": next_letter_id(state),
        "patientId": "pat_7",
        "conversationId": conv_id,
        "direction": "to_patient",
        "subject": "Asthma Follow-up Scheduling",
        "body": "Hi David, please schedule your next spirometry test at your earliest convenience. We recommend testing every 6 months.",
        "category": None,
        "senderId": "prov_1",
        "senderType": "provider",
        "attachments": [],
        "postDate": None,
        "sentAt": TIMESTAMP,
        "readAt": None,
        "isRead": False,
        "isDraft": False,
        "conversationState": "open",
        "doNotAllowResponse": False,
        "unreadAlertTimeframe": "none",
        "printHeader": "default"
    })


def solve_task_8(state):
    """Send letter to Priya Sharma with do-not-allow-response."""
    conv_id = next_conversation_id(state)
    state["patientLetters"].append({
        "id": next_letter_id(state),
        "patientId": "pat_32",
        "conversationId": conv_id,
        "direction": "to_patient",
        "subject": "Medical Records Information",
        "body": "Hi Priya, please fill out the attached records release form and return it to our office. Processing takes 5-7 business days.",
        "category": None,
        "senderId": "prov_1",
        "senderType": "provider",
        "attachments": [],
        "postDate": None,
        "sentAt": TIMESTAMP,
        "readAt": None,
        "isRead": False,
        "isDraft": False,
        "conversationState": "open",
        "doNotAllowResponse": True,
        "unreadAlertTimeframe": "none",
        "printHeader": "default"
    })


def solve_task_9(state):
    """Delete the draft letter ltr_35."""
    state["patientLetters"] = [l for l in state["patientLetters"] if l["id"] != "ltr_35"]


def solve_task_10(state):
    """Send the draft letter ltr_35."""
    letter = find_letter(state, "ltr_35")
    letter["isDraft"] = False
    letter["sentAt"] = TIMESTAMP


def solve_task_11(state):
    """Add 'VIP' tag to David Park."""
    patient = find_patient_by_name(state, "David", "Park")
    if "VIP" not in patient["tags"]:
        patient["tags"].append("VIP")


def solve_task_12(state):
    """Add 'High Risk' tag to Janet Okonkwo."""
    patient = find_patient_by_name(state, "Janet", "Okonkwo")
    if "High Risk" not in patient["tags"]:
        patient["tags"].append("High Risk")


def solve_task_13(state):
    """Add 'Insurance Pending' tag to Megan Burke."""
    patient = find_patient_by_name(state, "Megan", "Burke")
    if "Insurance Pending" not in patient["tags"]:
        patient["tags"].append("Insurance Pending")


def solve_task_14(state):
    """Remove 'New Patient' tag from Emily Thompson."""
    patient = find_patient_by_name(state, "Emily", "Thompson")
    patient["tags"] = [t for t in patient["tags"] if t != "New Patient"]


def solve_task_15(state):
    """Remove 'Chronic Care' tag from Robert Washington."""
    patient = find_patient_by_name(state, "Robert", "Washington")
    patient["tags"] = [t for t in patient["tags"] if t != "Chronic Care"]


def solve_task_16(state):
    """Toggle SMS opt-in for David Park to opted_out."""
    patient = find_patient_by_name(state, "David", "Park")
    patient["smsOptInStatus"] = "opted_out"


def solve_task_17(state):
    """Toggle SMS opt-in for Robert Washington to opted_in."""
    patient = find_patient_by_name(state, "Robert", "Washington")
    patient["smsOptInStatus"] = "opted_in"


def solve_task_18(state):
    """Update Brian Murphy's email."""
    patient = find_patient_by_name(state, "Brian", "Murphy")
    patient["email"] = "brian.murphy@gmail.com"


def solve_task_19(state):
    """Update Alice Johansson's phone."""
    patient = find_patient_by_name(state, "Alice", "Johansson")
    patient["cellPhone"] = "(415) 555-9999"


def solve_task_20(state):
    """Add emergency contact for Kevin Adebayo."""
    patient = find_patient_by_name(state, "Kevin", "Adebayo")
    patient["emergencyContact"] = {
        "name": "Grace Adebayo",
        "phone": "(650) 555-1122",
        "relationship": "Wife"
    }


def solve_task_21(state):
    """Send passport invitation to Anthony Petrov."""
    patient = find_patient_by_name(state, "Anthony", "Petrov")
    patient["passportStatus"] = "invited"
    patient["invitedAt"] = TIMESTAMP
    patient["invitationCode"] = "9999999"


def solve_task_22(state):
    """Send passport invitation to Brian Murphy."""
    patient = find_patient_by_name(state, "Brian", "Murphy")
    patient["passportStatus"] = "invited"
    patient["invitedAt"] = TIMESTAMP
    patient["invitationCode"] = "9999998"


def solve_task_23(state):
    """Send passport invitation to Megan Burke."""
    patient = find_patient_by_name(state, "Megan", "Burke")
    patient["passportStatus"] = "invited"
    patient["invitedAt"] = TIMESTAMP
    patient["invitationCode"] = "9999997"


def solve_task_24(state):
    """Resend passport invitation to Marcus Johnson."""
    patient = find_patient_by_name(state, "Marcus", "Johnson")
    patient["invitedAt"] = TIMESTAMP
    patient["invitationCode"] = "8888888"


def solve_task_25(state):
    """Resend passport invitation to William Chang."""
    patient = find_patient_by_name(state, "William", "Chang")
    patient["invitedAt"] = TIMESTAMP
    patient["invitationCode"] = "8888887"


def solve_task_26(state):
    """Disable passport for Stephanie Rivera."""
    patient = find_patient_by_name(state, "Stephanie", "Rivera")
    patient["passportAccountDisabled"] = True
    patient["passportStatus"] = "not_invited"


def solve_task_27(state):
    """Change passport sharing level for James Rodriguez to 4."""
    patient = find_patient_by_name(state, "James", "Rodriguez")
    patient["passportSharingLevel"] = 4


def solve_task_28(state):
    """Change passport sharing level for Helen Matsumoto to 1."""
    patient = find_patient_by_name(state, "Helen", "Matsumoto")
    patient["passportSharingLevel"] = 1


def solve_task_29(state):
    """Schedule in-person appointment for Emily Thompson with Dr. Chen."""
    patient = find_patient_by_name(state, "Emily", "Thompson")
    state["appointments"].append({
        "id": next_appointment_id(state),
        "patientId": patient["id"],
        "providerId": "prov_1",
        "date": "2026-03-15T10:00:00Z",
        "place": "in_person",
        "status": "scheduled",
        "virtualVisitInstructions": None,
        "reason": "General check-up"
    })


def solve_task_30(state):
    """Schedule virtual appointment for Andrew McIntyre with Dr. Torres."""
    patient = find_patient_by_name(state, "Andrew", "McIntyre")
    state["appointments"].append({
        "id": next_appointment_id(state),
        "patientId": patient["id"],
        "providerId": "prov_2",
        "date": "2026-03-20T15:00:00Z",
        "place": "virtual",
        "status": "scheduled",
        "virtualVisitInstructions": "Join at https://zoom.us/j/7261048395?pwd=def456",
        "reason": "GI follow-up consultation"
    })


def solve_task_31(state):
    """Cancel Thomas Nakamura's cardiac monitoring appointment."""
    appt = find_appointment_by_patient_reason(state, "pat_17", "Cardiac monitoring")
    appt["status"] = "cancelled"


def solve_task_32(state):
    """Cancel Dennis Volkov's blood pressure management appointment."""
    appt = find_appointment_by_patient_reason(state, "pat_47", "Blood pressure")
    appt["status"] = "cancelled"


def solve_task_33(state):
    """Cancel Sophia Nguyen's thyroid check-up appointment."""
    appt = find_appointment_by_patient_reason(state, "pat_4", "Thyroid")
    appt["status"] = "cancelled"


def solve_task_34(state):
    """Acknowledge reminder rem_1."""
    reminder = find_reminder(state, "rem_1")
    reminder["acknowledged"] = True


def solve_task_35(state):
    """Acknowledge reminder rem_4."""
    reminder = find_reminder(state, "rem_4")
    reminder["acknowledged"] = True


def solve_task_36(state):
    """Acknowledge reminder rem_5."""
    reminder = find_reminder(state, "rem_5")
    reminder["acknowledged"] = True


def solve_task_37(state):
    """Acknowledge reminder rem_7."""
    reminder = find_reminder(state, "rem_7")
    reminder["acknowledged"] = True


def solve_task_38(state):
    """Acknowledge reminder rem_10."""
    reminder = find_reminder(state, "rem_10")
    reminder["acknowledged"] = True


def solve_task_39(state):
    """Change Dr. Chen's sharing default to 3."""
    provider = find_provider(state, "prov_1")
    provider["sharingDefault"] = 3


def solve_task_40(state):
    """Change Dr. Chen's notification timeframe to 72_hours."""
    provider = find_provider(state, "prov_1")
    provider["notificationTimeframe"] = "72_hours"


def solve_task_41(state):
    """Change Dr. Torres's notification timeframe to none."""
    provider = find_provider(state, "prov_2")
    provider["notificationTimeframe"] = "none"


def solve_task_42(state):
    """Disable patient messaging."""
    state["practiceSettings"]["allowPatientMessaging"] = False


def solve_task_43(state):
    """Disable booking site auto-invite."""
    state["practiceSettings"]["bookingSiteAutoInvite"] = False


def solve_task_44(state):
    """Add Clinical Team (ug_2) to Dr. Chen's Test Results routing."""
    routing = state["messageRouting"]["prov_1"]["Test Results"]
    if "ug_2" not in routing:
        routing.append("ug_2")


def solve_task_45(state):
    """Remove Front Desk (ug_1) from Dr. Torres's General Question routing."""
    routing = state["messageRouting"]["prov_2"]
    routing["General Question"] = [r for r in routing["General Question"] if r != "ug_1"]


def solve_task_46(state):
    """Add Nurses (ug_3) to Dr. Kim's Prescription Refill routing."""
    routing = state["messageRouting"]["prov_4"]["Prescription Refill"]
    if "ug_3" not in routing:
        routing.append("ug_3")


def solve_task_47(state):
    """Activate virtual visit for Jessica Okafor with instructions."""
    provider = find_provider(state, "prov_3")
    provider["virtualVisitActivated"] = True
    provider["virtualVisitInstructions"] = "Join your telehealth visit at https://zoom.us/j/1234567890. Please test your camera and microphone beforehand."


def solve_task_48(state):
    """Deactivate virtual visit for Dr. Torres."""
    provider = find_provider(state, "prov_2")
    provider["virtualVisitActivated"] = False


def solve_task_49(state):
    """Update Dr. Kim's virtual visit instructions."""
    provider = find_provider(state, "prov_4")
    provider["virtualVisitInstructions"] = "Please join via https://zoom.us/j/9999999999. Test your camera before the visit."


def solve_task_50(state):
    """Disable screen sharing for patients."""
    state["practiceSettings"]["videoSettings"]["screenSharingPatients"] = False


def solve_task_51(state):
    """Disable waiting room audio notification."""
    state["practiceSettings"]["videoSettings"]["waitingRoomAudioNotification"] = False


def solve_task_52(state):
    """Change video chat mode to host_only."""
    state["practiceSettings"]["videoSettings"]["chatMode"] = "host_only"


def solve_task_53(state):
    """Add South Bay Clinic practice location."""
    state["practiceSettings"]["practiceLocations"].append({
        "id": next_location_id(state),
        "name": "South Bay Clinic",
        "address": "789 Stevens Creek Blvd, San Jose, CA 95128",
        "posCode": "11",
        "posDescription": "Office"
    })


def solve_task_54(state):
    """Remove East Bay Clinic practice location."""
    state["practiceSettings"]["practiceLocations"] = [
        loc for loc in state["practiceSettings"]["practiceLocations"]
        if loc["name"] != "East Bay Clinic"
    ]


def solve_task_55(state):
    """Add CPT code 99205."""
    state["practiceSettings"]["cptCodes"].append({
        "code": "99205",
        "description": "Office visit, new patient, high complexity"
    })


def solve_task_56(state):
    """Remove CPT code 99201."""
    state["practiceSettings"]["cptCodes"] = [
        c for c in state["practiceSettings"]["cptCodes"]
        if c["code"] != "99201"
    ]


def solve_task_57(state):
    """Update Main Office location name to SF Main Office."""
    loc = find_location_by_name(state, "Main Office")
    loc["name"] = "SF Main Office"


def solve_task_58(state):
    """Send bulk letter to James Rodriguez and Emily Thompson."""
    pat_1 = find_patient_by_name(state, "James", "Rodriguez")
    pat_2 = find_patient_by_name(state, "Emily", "Thompson")
    target_ids = [pat_1["id"], pat_2["id"]]

    bulk_id = next_bulk_letter_id(state)
    state["bulkLetters"].append({
        "id": bulk_id,
        "description": "Annual Wellness Reminder",
        "subject": "Schedule Your Annual Wellness Visit",
        "body": "Dear patient, please schedule your annual wellness visit at your earliest convenience. Contact our office to book an appointment.",
        "sentAt": TIMESTAMP,
        "sentBy": "prov_1",
        "targetCount": 2,
        "allowResponse": True
    })

    conv_id = next_conversation_id(state)
    for pat_id in target_ids:
        state["patientLetters"].append({
            "id": next_letter_id(state),
            "patientId": pat_id,
            "conversationId": f"{conv_id}_{pat_id}",
            "direction": "to_patient",
            "subject": "Schedule Your Annual Wellness Visit",
            "body": "Dear patient, please schedule your annual wellness visit at your earliest convenience. Contact our office to book an appointment.",
            "category": None,
            "senderId": "prov_1",
            "senderType": "provider",
            "attachments": [],
            "postDate": None,
            "sentAt": TIMESTAMP,
            "readAt": None,
            "isRead": False,
            "isDraft": False,
            "conversationState": "open",
            "doNotAllowResponse": False,
            "unreadAlertTimeframe": "none",
            "printHeader": "default"
        })


SOLVERS = {
    "task_1": solve_task_1,
    "task_2": solve_task_2,
    "task_3": solve_task_3,
    "task_4": solve_task_4,
    "task_5": solve_task_5,
    "task_6": solve_task_6,
    "task_7": solve_task_7,
    "task_8": solve_task_8,
    "task_9": solve_task_9,
    "task_10": solve_task_10,
    "task_11": solve_task_11,
    "task_12": solve_task_12,
    "task_13": solve_task_13,
    "task_14": solve_task_14,
    "task_15": solve_task_15,
    "task_16": solve_task_16,
    "task_17": solve_task_17,
    "task_18": solve_task_18,
    "task_19": solve_task_19,
    "task_20": solve_task_20,
    "task_21": solve_task_21,
    "task_22": solve_task_22,
    "task_23": solve_task_23,
    "task_24": solve_task_24,
    "task_25": solve_task_25,
    "task_26": solve_task_26,
    "task_27": solve_task_27,
    "task_28": solve_task_28,
    "task_29": solve_task_29,
    "task_30": solve_task_30,
    "task_31": solve_task_31,
    "task_32": solve_task_32,
    "task_33": solve_task_33,
    "task_34": solve_task_34,
    "task_35": solve_task_35,
    "task_36": solve_task_36,
    "task_37": solve_task_37,
    "task_38": solve_task_38,
    "task_39": solve_task_39,
    "task_40": solve_task_40,
    "task_41": solve_task_41,
    "task_42": solve_task_42,
    "task_43": solve_task_43,
    "task_44": solve_task_44,
    "task_45": solve_task_45,
    "task_46": solve_task_46,
    "task_47": solve_task_47,
    "task_48": solve_task_48,
    "task_49": solve_task_49,
    "task_50": solve_task_50,
    "task_51": solve_task_51,
    "task_52": solve_task_52,
    "task_53": solve_task_53,
    "task_54": solve_task_54,
    "task_55": solve_task_55,
    "task_56": solve_task_56,
    "task_57": solve_task_57,
    "task_58": solve_task_58,
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
    """Reset → solve → verify for a single task."""
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
    parser = argparse.ArgumentParser(description="Elation Patient Communication function-task sanity check")
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
