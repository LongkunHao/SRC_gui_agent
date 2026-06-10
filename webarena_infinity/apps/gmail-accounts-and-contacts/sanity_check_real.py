#!/usr/bin/env python3
"""
Sanity check for Gmail Accounts & Contacts real-task verifiers.

For each task, directly applies the expected end-state (bypassing the agent),
then runs the verifier and asserts it passes.

Usage:
    python3 sanity_check_real.py                      # All tasks, sequential
    python3 sanity_check_real.py --workers N           # N parallel environments
    python3 sanity_check_real.py --task-id task_e1     # Single task
    python3 sanity_check_real.py --port 9500           # Custom base port
"""
import argparse
import importlib.util
import json
import os
import socket
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path

import requests

APP_DIR = Path(__file__).resolve().parent
TASKS_FILE = APP_DIR / "real-tasks.json"

# JS snippet to evaluate data.js and emit the seed state as JSON
_SEED_STATE_JS = """
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync(process.argv[1], 'utf8');
vm.runInThisContext(code);

const state = {
    contacts: JSON.parse(JSON.stringify(CONTACTS)),
    otherContacts: JSON.parse(JSON.stringify(OTHER_CONTACTS)),
    contactLabels: JSON.parse(JSON.stringify(CONTACT_LABELS)),
    delegates: JSON.parse(JSON.stringify(DELEGATES)),
    linkedServices: JSON.parse(JSON.stringify(LINKED_SERVICES)),
    alwaysLinkedServices: JSON.parse(JSON.stringify(ALWAYS_LINKED_SERVICES)),
    accountSettings: JSON.parse(JSON.stringify(ACCOUNT_SETTINGS)),
    currentUser: JSON.parse(JSON.stringify(CURRENT_USER)),
    contactHistory: JSON.parse(JSON.stringify(CONTACT_HISTORY)),
    importExportHistory: JSON.parse(JSON.stringify(IMPORT_EXPORT_HISTORY)),
    mergeSuggestions: JSON.parse(JSON.stringify(MERGE_SUGGESTIONS)),
    _nextContactId: 50,
    _nextOtherContactId: 30,
    _nextLabelId: 20,
    _nextDelegateId: 10,
    _nextHistoryId: 20,
};
process.stdout.write(JSON.stringify(state));
"""


# ── helpers ──────────────────────────────────────────────────────────

def find_contact(state, firstName, lastName):
    for c in state["contacts"]:
        if c["firstName"] == firstName and c["lastName"] == lastName:
            return c
    raise ValueError(f"Contact not found: {firstName} {lastName}")


def find_contact_by_email(state, email):
    for c in state["contacts"]:
        if c["email"] == email:
            return c
    raise ValueError(f"Contact not found: {email}")


def find_other_contact(state, email):
    for c in state["otherContacts"]:
        if c["email"] == email:
            return c
    raise ValueError(f"Other contact not found: {email}")


def find_label(state, name):
    for l in state["contactLabels"]:
        if l["name"] == name:
            return l
    raise ValueError(f"Label not found: {name}")


def find_label_by_id(state, label_id):
    for l in state["contactLabels"]:
        if l["id"] == label_id:
            return l
    raise ValueError(f"Label not found: {label_id}")


def find_delegate(state, email):
    for d in state["delegates"]:
        if d["email"] == email:
            return d
    raise ValueError(f"Delegate not found: {email}")


def find_service(state, name):
    for s in state["linkedServices"]:
        if s["name"] == name:
            return s
    raise ValueError(f"Service not found: {name}")


def find_merge(state, merge_id):
    for m in state["mergeSuggestions"]:
        if m["id"] == merge_id:
            return m
    raise ValueError(f"Merge suggestion not found: {merge_id}")


def next_contact_id(state):
    nid = state["_nextContactId"]
    state["_nextContactId"] = nid + 1
    return nid


def next_label_id(state):
    nid = state["_nextLabelId"]
    state["_nextLabelId"] = nid + 1
    return nid


def next_delegate_id(state):
    nid = state["_nextDelegateId"]
    state["_nextDelegateId"] = nid + 1
    return nid


NOW = "2026-03-08T12:00:00Z"


# ── easy solve functions ─────────────────────────────────────────────

def solve_task_e1(state):
    """Star James O'Brien."""
    c = find_contact(state, "James", "O'Brien")
    c["isStarred"] = True


def solve_task_e2(state):
    """Turn off auto-save contacts."""
    state["accountSettings"]["autoSaveContacts"] = False


def solve_task_e3(state):
    """Remove the expired delegate."""
    state["delegates"] = [d for d in state["delegates"] if d["status"] != "expired"]


def solve_task_e4(state):
    """Disable activity tracking."""
    state["accountSettings"]["privacySettings"]["activityTracking"] = False


def solve_task_e5(state):
    """Unlink YouTube."""
    svc = find_service(state, "YouTube")
    svc["isLinked"] = False


def solve_task_e6(state):
    """Delete Diana Castillo."""
    state["contacts"] = [c for c in state["contacts"]
                         if not (c["firstName"] == "Diana" and c["lastName"] == "Castillo")]


def solve_task_e7(state):
    """Dismiss the CloudNine merge suggestion."""
    merge = find_merge(state, "merge_1")
    merge["dismissed"] = True


def solve_task_e8(state):
    """Turn on contact changes notifications."""
    state["accountSettings"]["notificationSettings"]["contactChanges"] = True


def solve_task_e9(state):
    """Switch 2FA method to SMS."""
    state["accountSettings"]["loginSettings"]["twoFactorMethod"] = "sms"


def solve_task_e10(state):
    """Unstar Emily Rodriguez."""
    c = find_contact(state, "Emily", "Rodriguez")
    c["isStarred"] = False


def solve_task_e11(state):
    """Delete the College Alumni label."""
    label_id = "clabel_6"
    state["contactLabels"] = [l for l in state["contactLabels"] if l["id"] != label_id]
    for c in state["contacts"]:
        c["labels"] = [lid for lid in c["labels"] if lid != label_id]


def solve_task_e12(state):
    """Remove AWS Billing from other contacts."""
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "billing@aws.amazon.com"]


def solve_task_e13(state):
    """Link Google Ads."""
    svc = find_service(state, "Google Ads")
    svc["isLinked"] = True


def solve_task_e14(state):
    """Turn off calendar sync."""
    state["accountSettings"]["syncSettings"]["calendarSync"] = False


def solve_task_e15(state):
    """Make phone number visible to everyone."""
    state["accountSettings"]["privacySettings"]["showPhone"] = "everyone"


def solve_task_e16(state):
    """Change contact sort order to last name."""
    state["accountSettings"]["contactsSortBy"] = "lastName"


def solve_task_e17(state):
    """Turn off linked service update notifications."""
    state["accountSettings"]["notificationSettings"]["linkedServiceUpdates"] = False


def solve_task_e18(state):
    """Disable two-factor authentication."""
    state["accountSettings"]["loginSettings"]["twoFactorEnabled"] = False


def solve_task_e19(state):
    """Remove Stripe Notifications from other contacts."""
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "no-reply@stripe.com"]


def solve_task_e20(state):
    """Rename Emergency label to Urgent."""
    l = find_label_by_id(state, "clabel_10")
    l["name"] = "Urgent"


# ── medium solve functions ───────────────────────────────────────────

def solve_task_m1(state):
    """Update name to Alexander Johnson and recovery email."""
    state["currentUser"]["name"] = "Alexander Johnson"
    state["currentUser"]["recoveryEmail"] = "alex.secure@proton.me"


def solve_task_m2(state):
    """Create contact Jordan Wells."""
    nid = next_contact_id(state)
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": "Jordan", "lastName": "Wells",
        "email": "jordan.wells@wellsfargo.com", "phone": "",
        "company": "Wells Fargo", "jobTitle": "", "address": "",
        "secondaryEmail": "", "secondaryPhone": "", "birthday": "",
        "website": "", "notes": "", "labels": [], "isStarred": False,
        "avatarColor": "#EA4335", "createdAt": NOW, "updatedAt": NOW,
        "source": "manual"
    })


def solve_task_m3(state):
    """Add delegate ops@techcorp.io."""
    nid = next_delegate_id(state)
    state["delegates"].append({
        "id": f"delegate_{nid}",
        "email": "ops@techcorp.io",
        "name": "TechCorp Ops",
        "status": "pending",
        "addedAt": NOW,
        "activatedAt": None,
        "permissions": {
            "readEmail": True, "sendEmail": True, "deleteEmail": True,
            "manageChat": False, "changePassword": False
        }
    })


def solve_task_m4(state):
    """Rename Gym Buddies to Fitness and change color to #4285F4."""
    l = find_label_by_id(state, "clabel_5")
    l["name"] = "Fitness"
    l["color"] = "#4285F4"


def solve_task_m5(state):
    """Move Jason Blake from other contacts to main contacts."""
    other = find_other_contact(state, "jason.blake@salesforce.com")
    nid = next_contact_id(state)
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": other.get("firstName", ""),
        "lastName": other.get("lastName", ""),
        "email": other["email"], "phone": "", "company": "",
        "jobTitle": "", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "",
        "notes": "Auto-saved contact moved to main contacts.",
        "labels": [], "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": NOW, "updatedAt": NOW, "source": "auto-promoted"
    })
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "jason.blake@salesforce.com"]


def solve_task_m6(state):
    """Turn off all four notification types."""
    ns = state["accountSettings"]["notificationSettings"]
    ns["delegateActivity"] = False
    ns["contactChanges"] = False
    ns["securityAlerts"] = False
    ns["linkedServiceUpdates"] = False


def solve_task_m7(state):
    """Remove pending and expired delegates."""
    state["delegates"] = [d for d in state["delegates"]
                          if d["status"] not in ("pending", "expired")]


def solve_task_m8(state):
    """Create label Project Alpha and assign to Sarah Chen."""
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Project Alpha",
        "color": "#757575", "contactCount": 0
    })
    c = find_contact(state, "Sarah", "Chen")
    if label_id not in c["labels"]:
        c["labels"].append(label_id)


def solve_task_m9(state):
    """Update Tom Bradley email and job title."""
    c = find_contact(state, "Tom", "Bradley")
    c["email"] = "tom@newrealty.com"
    c["jobTitle"] = "Senior Agent"


def solve_task_m10(state):
    """Merge EuroDesign duplicate contacts."""
    merge = find_merge(state, "merge_2")
    primary = find_contact(state, "Sophie", "Laurent")
    secondary = find_contact(state, "Elena", "Volkov")
    # Merge secondary into primary
    if not primary["secondaryEmail"] and secondary["email"]:
        primary["secondaryEmail"] = secondary["email"]
    if not primary["secondaryPhone"] and secondary["phone"]:
        primary["secondaryPhone"] = secondary["phone"]
    for lbl in secondary["labels"]:
        if lbl not in primary["labels"]:
            primary["labels"].append(lbl)
    if secondary["notes"] and secondary["notes"] not in primary["notes"]:
        primary["notes"] = (primary["notes"] + "\n" + secondary["notes"]
                            if primary["notes"] else secondary["notes"])
    state["contacts"] = [c for c in state["contacts"] if c["id"] != secondary["id"]]
    merge["dismissed"] = True


def solve_task_m11(state):
    """Sort by last name and display order last name first."""
    state["accountSettings"]["contactsSortBy"] = "lastName"
    state["accountSettings"]["contactsDisplayOrder"] = "lastFirst"


def solve_task_m12(state):
    """Unlink Google Maps and Chrome."""
    find_service(state, "Google Maps")["isLinked"] = False
    find_service(state, "Chrome")["isLinked"] = False


def solve_task_m13(state):
    """Set profile photo and email visibility to Nobody."""
    ps = state["accountSettings"]["privacySettings"]
    ps["showProfilePhoto"] = "nobody"
    ps["showEmail"] = "nobody"


def solve_task_m14(state):
    """Delete Dr. Patricia Nguyen and Mike Chen."""
    state["contacts"] = [c for c in state["contacts"]
                         if not (c["firstName"] == "Dr. Patricia" and c["lastName"] == "Nguyen")
                         and not (c["firstName"] == "Mike" and c["lastName"] == "Chen")]


def solve_task_m15(state):
    """Star Ben Walker and Tony Russo."""
    find_contact(state, "Ben", "Walker")["isStarred"] = True
    find_contact(state, "Tony", "Russo")["isStarred"] = True


def solve_task_m16(state):
    """Update Sarah Chen company and title."""
    c = find_contact(state, "Sarah", "Chen")
    c["company"] = "TechCorp Global"
    c["jobTitle"] = "SVP of Product"


def solve_task_m17(state):
    """Disable auto-save contacts and show contact info."""
    state["accountSettings"]["autoSaveContacts"] = False
    state["accountSettings"]["collaborationSettings"]["showContactInfo"] = False


def solve_task_m18(state):
    """Move Tina Marshall and delete Chloe Bennett."""
    # Move Tina Marshall
    other = find_other_contact(state, "tina.marshall@designhub.com")
    nid = next_contact_id(state)
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": other.get("firstName", ""),
        "lastName": other.get("lastName", ""),
        "email": other["email"], "phone": "", "company": "",
        "jobTitle": "", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "",
        "notes": "Auto-saved contact moved to main contacts.",
        "labels": [], "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": NOW, "updatedAt": NOW, "source": "auto-promoted"
    })
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "tina.marshall@designhub.com"]
    # Delete Chloe Bennett
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] != "chloe.b@sequoiacap.com"]


def solve_task_m19(state):
    """Create label Investors with #FF5722 and add to Emily Rodriguez."""
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Investors",
        "color": "#FF5722", "contactCount": 0
    })
    c = find_contact(state, "Emily", "Rodriguez")
    if label_id not in c["labels"]:
        c["labels"].append(label_id)


def solve_task_m20(state):
    """Switch to security key 2FA and turn off remember password."""
    ls = state["accountSettings"]["loginSettings"]
    ls["twoFactorMethod"] = "security_key"
    ls["rememberPassword"] = False


# ── hard solve functions ─────────────────────────────────────────────

def solve_task_h1(state):
    """Remove all non-active delegates and add backup@admin.com."""
    state["delegates"] = [d for d in state["delegates"] if d["status"] == "active"]
    nid = next_delegate_id(state)
    state["delegates"].append({
        "id": f"delegate_{nid}",
        "email": "backup@admin.com",
        "name": "Backup Admin",
        "status": "pending",
        "addedAt": NOW,
        "activatedAt": None,
        "permissions": {
            "readEmail": True, "sendEmail": True, "deleteEmail": True,
            "manageChat": False, "changePassword": False
        }
    })


def solve_task_h2(state):
    """Invert all Google service link states."""
    for svc in state["linkedServices"]:
        svc["isLinked"] = not svc["isLinked"]


def solve_task_h3(state):
    """Delete all TechCorp contacts."""
    state["contacts"] = [c for c in state["contacts"] if c.get("company") != "TechCorp"]


def solve_task_h4(state):
    """All Family contacts get Emergency and Friends labels."""
    for c in state["contacts"]:
        if "clabel_1" in c["labels"]:
            if "clabel_10" not in c["labels"]:
                c["labels"].append("clabel_10")
            if "clabel_2" not in c["labels"]:
                c["labels"].append("clabel_2")


def solve_task_h5(state):
    """Create Collaborators label and add to CloudNine/DesignHub contacts."""
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Collaborators",
        "color": "#757575", "contactCount": 0
    })
    for c in state["contacts"]:
        if c.get("company") in ("CloudNine", "DesignHub"):
            if label_id not in c["labels"]:
                c["labels"].append(label_id)


def solve_task_h6(state):
    """All visibility to Nobody, disable tracking, turn off all notifications."""
    ps = state["accountSettings"]["privacySettings"]
    ps["showProfilePhoto"] = "nobody"
    ps["showEmail"] = "nobody"
    ps["showPhone"] = "nobody"
    ps["activityTracking"] = False
    ns = state["accountSettings"]["notificationSettings"]
    ns["delegateActivity"] = False
    ns["contactChanges"] = False
    ns["securityAlerts"] = False
    ns["linkedServiceUpdates"] = False


def solve_task_h7(state):
    """Delete auto-saved contacts with no-reply/do-not-reply emails."""
    noreply_emails = {
        "no-reply@stripe.com",
        "noreply@github.com",
        "do-not-reply@zoom.us",
        "no-reply@docusign.net",
    }
    state["otherContacts"] = [c for c in state["otherContacts"]
                              if c["email"] not in noreply_emails]


def solve_task_h8(state):
    """Delete all Vendor contacts and delete the Vendors label."""
    # Delete contacts with Vendors label
    state["contacts"] = [c for c in state["contacts"]
                         if "clabel_9" not in c.get("labels", [])]
    # Delete the Vendors label
    state["contactLabels"] = [l for l in state["contactLabels"] if l["id"] != "clabel_9"]
    # Clean up any remaining references
    for c in state["contacts"]:
        c["labels"] = [lid for lid in c["labels"] if lid != "clabel_9"]


def solve_task_h9(state):
    """Unstar all starred contacts except Family."""
    for c in state["contacts"]:
        if c["isStarred"] and "clabel_1" not in c.get("labels", []):
            c["isStarred"] = False


def solve_task_h10(state):
    """Create Tech label and add to companies with 'Tech' in name."""
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Tech",
        "color": "#757575", "contactCount": 0
    })
    for c in state["contacts"]:
        company = c.get("company", "")
        if "Tech" in company:
            if label_id not in c["labels"]:
                c["labels"].append(label_id)


def solve_task_h11(state):
    """Maximum security settings."""
    ls = state["accountSettings"]["loginSettings"]
    ls["twoFactorEnabled"] = True
    ls["twoFactorMethod"] = "security_key"
    ls["rememberPassword"] = False
    ls["autoSignIn"] = False
    ps = state["accountSettings"]["privacySettings"]
    ps["showProfilePhoto"] = "nobody"
    ps["showEmail"] = "nobody"
    ps["showPhone"] = "nobody"
    ps["activityTracking"] = False


def solve_task_h12(state):
    """Merge CloudNine, dismiss EuroDesign, remove pending delegate."""
    # Merge CloudNine (merge_1): Priya Sharma + Raj Kapoor
    merge1 = find_merge(state, "merge_1")
    primary = find_contact(state, "Priya", "Sharma")
    secondary = find_contact(state, "Raj", "Kapoor")
    if not primary["secondaryEmail"] and secondary["email"]:
        primary["secondaryEmail"] = secondary["email"]
    if not primary["secondaryPhone"] and secondary["phone"]:
        primary["secondaryPhone"] = secondary["phone"]
    for lbl in secondary["labels"]:
        if lbl not in primary["labels"]:
            primary["labels"].append(lbl)
    if secondary["notes"] and secondary["notes"] not in primary["notes"]:
        primary["notes"] = (primary["notes"] + "\n" + secondary["notes"]
                            if primary["notes"] else secondary["notes"])
    state["contacts"] = [c for c in state["contacts"] if c["id"] != secondary["id"]]
    merge1["dismissed"] = True

    # Dismiss EuroDesign (merge_2)
    merge2 = find_merge(state, "merge_2")
    merge2["dismissed"] = True

    # Remove pending delegate
    state["delegates"] = [d for d in state["delegates"] if d["status"] != "pending"]


def solve_task_h13(state):
    """EuroDesign contacts: remove Work, add VIP Clients."""
    sophie = find_contact(state, "Sophie", "Laurent")
    elena = find_contact(state, "Elena", "Volkov")
    for c in [sophie, elena]:
        c["labels"] = [lid for lid in c["labels"] if lid != "clabel_3"]
        if "clabel_4" not in c["labels"]:
            c["labels"].append("clabel_4")


def solve_task_h14(state):
    """Delete all non-US contacts."""
    non_us_names = [
        ("Sophie", "Laurent"),
        ("Yuki", "Tanaka"),
        ("Raj", "Kapoor"),
        ("Elena", "Volkov"),
    ]
    for fn, ln in non_us_names:
        state["contacts"] = [c for c in state["contacts"]
                             if not (c["firstName"] == fn and c["lastName"] == ln)]


def solve_task_h15(state):
    """Delete Book Club and Gym Buddies labels, add Friends to affected contacts."""
    # Contacts that had Book Club (clabel_8) or Gym Buddies (clabel_5)
    # and need Friends (clabel_2) added:
    # Tony Russo (Book Club, no Friends)
    # Hannah Brooks (Gym Buddies, no Friends)
    # Diana Castillo (Gym Buddies, no Friends)
    needs_friends = {"contact_38", "contact_17", "contact_35"}
    for c in state["contacts"]:
        if c["id"] in needs_friends and "clabel_2" not in c["labels"]:
            c["labels"].append("clabel_2")
    # Delete the labels
    state["contactLabels"] = [l for l in state["contactLabels"]
                              if l["id"] not in ("clabel_8", "clabel_5")]
    # Remove label references from all contacts
    for c in state["contacts"]:
        c["labels"] = [lid for lid in c["labels"]
                       if lid not in ("clabel_8", "clabel_5")]


def solve_task_h16(state):
    """Unstar all, then star James O'Brien and David Kim."""
    for c in state["contacts"]:
        c["isStarred"] = False
    find_contact(state, "James", "O'Brien")["isStarred"] = True
    find_contact(state, "David", "Kim")["isStarred"] = True


def solve_task_h17(state):
    """Remove all delegates, disable delegate notifications, unlink all linked services."""
    state["delegates"] = []
    state["accountSettings"]["notificationSettings"]["delegateActivity"] = False
    for svc in state["linkedServices"]:
        if svc["isLinked"]:
            svc["isLinked"] = False


def solve_task_h18(state):
    """Star all Friends-labeled contacts who don't have Work label."""
    for c in state["contacts"]:
        if "clabel_2" in c.get("labels", []) and "clabel_3" not in c.get("labels", []):
            c["isStarred"] = True


def solve_task_h19(state):
    """All sync off, uncheck ack, all notifications off, tracking off."""
    ss = state["accountSettings"]["syncSettings"]
    ss["contactsSync"] = False
    ss["calendarSync"] = False
    ss["emailSync"] = False
    ss["googleSyncDeprecationAcknowledged"] = False
    ns = state["accountSettings"]["notificationSettings"]
    ns["delegateActivity"] = False
    ns["contactChanges"] = False
    ns["securityAlerts"] = False
    ns["linkedServiceUpdates"] = False
    state["accountSettings"]["privacySettings"]["activityTracking"] = False


def solve_task_h20(state):
    """Move all real people from other contacts to main contacts."""
    real_people_emails = [
        "jason.blake@salesforce.com",
        "tina.marshall@designhub.com",
        "alex.rivera@notion.so",
        "mike.santos@cloudflare.com",
        "wendy.chung@techcorp.io",
        "chloe.b@sequoiacap.com",
        "peter.grant@mongodb.com",
        "nina.k@figma.com",
    ]
    for email in real_people_emails:
        other = find_other_contact(state, email)
        nid = next_contact_id(state)
        state["contacts"].append({
            "id": f"contact_{nid:02d}",
            "firstName": other.get("firstName", ""),
            "lastName": other.get("lastName", ""),
            "email": other["email"], "phone": "", "company": "",
            "jobTitle": "", "address": "", "secondaryEmail": "",
            "secondaryPhone": "", "birthday": "", "website": "",
            "notes": "Auto-saved contact moved to main contacts.",
            "labels": [], "isStarred": False, "avatarColor": "#EA4335",
            "createdAt": NOW, "updatedAt": NOW, "source": "auto-promoted"
        })
        state["otherContacts"] = [c for c in state["otherContacts"]
                                  if c["email"] != email]


# ── hardening round 1 solve functions ────────────────────────────────

def solve_task_h21(state):
    """Remove delegates whose corresponding contact has the Work label."""
    contact_labels_by_email = {
        c["email"]: c.get("labels", []) for c in state["contacts"]
    }
    state["delegates"] = [
        d for d in state["delegates"]
        if "clabel_3" not in contact_labels_by_email.get(d["email"], [])
    ]


def solve_task_h22(state):
    """Remove Maya Patel's delegate access and unstar her contact."""
    state["delegates"] = [
        d for d in state["delegates"]
        if d["email"] != "maya.patel@techcorp.io"
    ]
    c = find_contact(state, "Maya", "Patel")
    c["isStarred"] = False


def solve_task_h23(state):
    """Add Emergency label to contact born March 8 (Emily Rodriguez)."""
    c = find_contact(state, "Emily", "Rodriguez")
    if "clabel_10" not in c["labels"]:
        c["labels"].append("clabel_10")


def solve_task_h24(state):
    """Move Tina Marshall (DesignHub, same as Marcus Williams) to main contacts."""
    other = find_other_contact(state, "tina.marshall@designhub.com")
    nid = next_contact_id(state)
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": other.get("firstName", ""),
        "lastName": other.get("lastName", ""),
        "email": other["email"], "phone": "", "company": "",
        "jobTitle": "", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "",
        "notes": "Auto-saved contact moved to main contacts.",
        "labels": [], "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": NOW, "updatedAt": NOW, "source": "auto-promoted"
    })
    state["otherContacts"] = [
        c for c in state["otherContacts"]
        if c["email"] != "tina.marshall@designhub.com"
    ]


def solve_task_h25(state):
    """Remove Work label from all CloudNine contacts (Priya Sharma's company)."""
    for c in state["contacts"]:
        if c.get("company") == "CloudNine":
            c["labels"] = [lid for lid in c["labels"] if lid != "clabel_3"]


def solve_task_h26(state):
    """Star all Neighbors, remove Neighbors from those also in Book Club."""
    for c in state["contacts"]:
        if "clabel_7" in c.get("labels", []):
            c["isStarred"] = True
            if "clabel_8" in c.get("labels", []):
                c["labels"] = [lid for lid in c["labels"] if lid != "clabel_7"]


def solve_task_h27(state):
    """Add VIP Clients to starred Work contacts who don't have it."""
    for c in state["contacts"]:
        if (c.get("isStarred")
                and "clabel_3" in c.get("labels", [])
                and "clabel_4" not in c.get("labels", [])):
            c["labels"].append("clabel_4")


def solve_task_h28(state):
    """Delete EuroDesign contacts, dismiss merge_2, delete Travel Contacts label."""
    state["contacts"] = [
        c for c in state["contacts"]
        if c.get("company") != "EuroDesign"
    ]
    merge2 = find_merge(state, "merge_2")
    merge2["dismissed"] = True
    state["contactLabels"] = [
        l for l in state["contactLabels"] if l["id"] != "clabel_11"
    ]
    for c in state["contacts"]:
        c["labels"] = [lid for lid in c["labels"] if lid != "clabel_11"]


def solve_task_h29(state):
    """Change profile name, create Priority label, add to Family contacts."""
    state["currentUser"]["name"] = "Alex J. Johnson"
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Priority",
        "color": "#EA4335", "contactCount": 0
    })
    for c in state["contacts"]:
        if "clabel_1" in c.get("labels", []):
            if label_id not in c["labels"]:
                c["labels"].append(label_id)


def solve_task_h30(state):
    """Delete Elena Volkov (UX Research Lead), star Sophie Laurent."""
    state["contacts"] = [
        c for c in state["contacts"]
        if not (c["firstName"] == "Elena" and c["lastName"] == "Volkov")
    ]
    c = find_contact(state, "Sophie", "Laurent")
    c["isStarred"] = True


def solve_task_h31(state):
    """Delete Mike Chen (dentist), update Sarah Chen title."""
    state["contacts"] = [
        c for c in state["contacts"]
        if not (c["firstName"] == "Mike" and c["lastName"] == "Chen")
    ]
    c = find_contact(state, "Sarah", "Chen")
    c["jobTitle"] = "Chief Product Officer"


def solve_task_h32(state):
    """Toggle star on each TechCorp contact."""
    for c in state["contacts"]:
        if c.get("company") == "TechCorp":
            c["isStarred"] = not c["isStarred"]


def solve_task_h33(state):
    """Move all @techcorp.io auto-saved contacts to main contacts."""
    techcorp_others = [
        c for c in state["otherContacts"]
        if c["email"].endswith("@techcorp.io")
    ]
    for other in techcorp_others:
        nid = next_contact_id(state)
        state["contacts"].append({
            "id": f"contact_{nid:02d}",
            "firstName": other.get("firstName", ""),
            "lastName": other.get("lastName", ""),
            "email": other["email"], "phone": "", "company": "",
            "jobTitle": "", "address": "", "secondaryEmail": "",
            "secondaryPhone": "", "birthday": "", "website": "",
            "notes": "Auto-saved contact moved to main contacts.",
            "labels": [], "isStarred": False, "avatarColor": "#EA4335",
            "createdAt": NOW, "updatedAt": NOW, "source": "auto-promoted"
        })
    state["otherContacts"] = [
        c for c in state["otherContacts"]
        if not c["email"].endswith("@techcorp.io")
    ]


def solve_task_h34(state):
    """Security key 2FA, disable auto sign-in/remember password, all visibility contacts_only."""
    ls = state["accountSettings"]["loginSettings"]
    ls["twoFactorMethod"] = "security_key"
    ls["autoSignIn"] = False
    ls["rememberPassword"] = False
    ps = state["accountSettings"]["privacySettings"]
    ps["showProfilePhoto"] = "contacts_only"
    ps["showEmail"] = "contacts_only"
    ps["showPhone"] = "contacts_only"


def solve_task_h35(state):
    """Remove expired Jake Morrison delegate and re-invite."""
    state["delegates"] = [
        d for d in state["delegates"]
        if d["email"] != "jake.morrison@gmail.com"
    ]
    nid = next_delegate_id(state)
    state["delegates"].append({
        "id": f"delegate_{nid}",
        "email": "jake.morrison@gmail.com",
        "name": "Jake Morrison",
        "status": "pending",
        "addedAt": NOW,
        "activatedAt": None,
        "permissions": {
            "readEmail": True, "sendEmail": True, "deleteEmail": True,
            "manageChat": False, "changePassword": False
        }
    })


def solve_task_h36(state):
    """Replace Healthcare with Emergency, delete Healthcare label."""
    for c in state["contacts"]:
        if "clabel_12" in c.get("labels", []):
            c["labels"] = [lid for lid in c["labels"] if lid != "clabel_12"]
            if "clabel_10" not in c["labels"]:
                c["labels"].append("clabel_10")
    state["contactLabels"] = [
        l for l in state["contactLabels"] if l["id"] != "clabel_12"
    ]


def solve_task_h37(state):
    """Move Alex Rivera, set company/title, add Work label."""
    other = find_other_contact(state, "alex.rivera@notion.so")
    nid = next_contact_id(state)
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": other.get("firstName", ""),
        "lastName": other.get("lastName", ""),
        "email": other["email"], "phone": "", "company": "Notion",
        "jobTitle": "Product Manager", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "",
        "notes": "", "labels": ["clabel_3"], "isStarred": False,
        "avatarColor": "#EA4335",
        "createdAt": NOW, "updatedAt": NOW, "source": "auto-promoted"
    })
    state["otherContacts"] = [
        c for c in state["otherContacts"]
        if c["email"] != "alex.rivera@notion.so"
    ]


def solve_task_h38(state):
    """Create Bay Area label, add to Menlo Park contacts."""
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Bay Area",
        "color": "#4285F4", "contactCount": 0
    })
    for c in state["contacts"]:
        if "Menlo Park" in c.get("address", ""):
            if label_id not in c["labels"]:
                c["labels"].append(label_id)


def solve_task_h39(state):
    """Unlink Chrome/Play, turn off contacts/email sync, disable auto-save."""
    find_service(state, "Chrome")["isLinked"] = False
    find_service(state, "Google Play")["isLinked"] = False
    state["accountSettings"]["syncSettings"]["contactsSync"] = False
    state["accountSettings"]["syncSettings"]["emailSync"] = False
    state["accountSettings"]["autoSaveContacts"] = False


def solve_task_h40(state):
    """Create Key Contacts for starred+VIP, remove VIP from unstarred."""
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Key Contacts",
        "color": "#FBBC04", "contactCount": 0
    })
    for c in state["contacts"]:
        has_vip = "clabel_4" in c.get("labels", [])
        if has_vip and c.get("isStarred"):
            if label_id not in c["labels"]:
                c["labels"].append(label_id)
        elif has_vip and not c.get("isStarred"):
            c["labels"] = [lid for lid in c["labels"] if lid != "clabel_4"]


# ── hardening round 2 solve functions ────────────────────────────────

def solve_task_h41(state):
    """Remove TechCorp delegates, add auto-saved TechCorp HR as delegate."""
    # VP of Product = Sarah Chen -> TechCorp -> @techcorp.io
    state["delegates"] = [
        d for d in state["delegates"]
        if not d["email"].endswith("@techcorp.io")
    ]
    nid = next_delegate_id(state)
    state["delegates"].append({
        "id": f"delegate_{nid}",
        "email": "hr@techcorp.io",
        "name": "TechCorp HR Team",
        "status": "pending",
        "addedAt": NOW,
        "activatedAt": None,
        "permissions": {
            "readEmail": True, "sendEmail": True, "deleteEmail": True,
            "manageChat": False, "changePassword": False
        }
    })


def solve_task_h42(state):
    """Non-US contacts: remove Work, ensure Travel Contacts."""
    non_us_names = [
        ("Sophie", "Laurent"),
        ("Yuki", "Tanaka"),
        ("Raj", "Kapoor"),
        ("Elena", "Volkov"),
    ]
    for fn, ln in non_us_names:
        c = find_contact(state, fn, ln)
        c["labels"] = [lid for lid in c["labels"] if lid != "clabel_3"]
        if "clabel_11" not in c["labels"]:
            c["labels"].append("clabel_11")


def solve_task_h43(state):
    """Nate Patel title change, Maya Patel gets VIP Clients."""
    nate = find_contact(state, "Nate", "Patel")
    nate["jobTitle"] = "Senior Infrastructure Lead"
    maya = find_contact(state, "Maya", "Patel")
    if "clabel_4" not in maya["labels"]:
        maya["labels"].append("clabel_4")


def solve_task_h44(state):
    """Star Leo Martinez (sister's husband) and add Friends."""
    c = find_contact(state, "Leo", "Martinez")
    c["isStarred"] = True
    if "clabel_2" not in c["labels"]:
        c["labels"].append("clabel_2")


def solve_task_h45(state):
    """Delete automated service other-contacts, move fewest-interaction person."""
    # Delete those with no firstName (automated services)
    state["otherContacts"] = [
        oc for oc in state["otherContacts"]
        if oc.get("firstName")
    ]
    # Fewest interactions among remaining: Chloe Bennett (1)
    other = find_other_contact(state, "chloe.b@sequoiacap.com")
    nid = next_contact_id(state)
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": other.get("firstName", ""),
        "lastName": other.get("lastName", ""),
        "email": other["email"], "phone": "", "company": "",
        "jobTitle": "", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "",
        "notes": "Auto-saved contact moved to main contacts.",
        "labels": [], "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": NOW, "updatedAt": NOW, "source": "auto-promoted"
    })
    state["otherContacts"] = [
        oc for oc in state["otherContacts"]
        if oc["email"] != "chloe.b@sequoiacap.com"
    ]


def solve_task_h46(state):
    """Star every contact whose only label is Work."""
    for c in state["contacts"]:
        if c.get("labels") == ["clabel_3"]:
            c["isStarred"] = True


def solve_task_h47(state):
    """Migrate Vendors to Work, delete Vendors label."""
    for c in state["contacts"]:
        if "clabel_9" in c.get("labels", []):
            c["labels"] = [lid for lid in c["labels"] if lid != "clabel_9"]
            if "clabel_3" not in c["labels"]:
                c["labels"].append("clabel_3")
    state["contactLabels"] = [
        l for l in state["contactLabels"] if l["id"] != "clabel_9"
    ]


def solve_task_h48(state):
    """Earliest-activated delegate -> update contact job title."""
    # Laura Johnson-Martinez activated 2024-12-02 (earliest)
    c = find_contact(state, "Laura", "Johnson-Martinez")
    c["jobTitle"] = "Senior Marketing Director"


def solve_task_h49(state):
    """Create Portland label, add to contacts with Portland address."""
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Portland",
        "color": "#009688", "contactCount": 0
    })
    for c in state["contacts"]:
        if "Portland" in c.get("address", ""):
            if label_id not in c["labels"]:
                c["labels"].append(label_id)


def solve_task_h50(state):
    """Add Emergency to delegate contacts, remove non-active delegates."""
    delegate_emails = {d["email"] for d in state["delegates"]}
    for c in state["contacts"]:
        if c["email"] in delegate_emails:
            if "clabel_10" not in c["labels"]:
                c["labels"].append("clabel_10")
    state["delegates"] = [
        d for d in state["delegates"] if d["status"] == "active"
    ]


def solve_task_h51(state):
    """Remove Friends from Work contacts, add Friends to Family contacts."""
    for c in state["contacts"]:
        if "clabel_2" in c.get("labels", []) and "clabel_3" in c.get("labels", []):
            c["labels"] = [lid for lid in c["labels"] if lid != "clabel_2"]
    for c in state["contacts"]:
        if "clabel_1" in c.get("labels", []) and "clabel_2" not in c.get("labels", []):
            c["labels"].append("clabel_2")


def solve_task_h52(state):
    """Photo visibility, unlink Maps, email sync off, Emergency to tax contact."""
    state["accountSettings"]["privacySettings"]["showProfilePhoto"] = "contacts_only"
    find_service(state, "Google Maps")["isLinked"] = False
    state["accountSettings"]["syncSettings"]["emailSync"] = False
    # David Kim handles tax prep
    david = find_contact(state, "David", "Kim")
    if "clabel_10" not in david["labels"]:
        david["labels"].append("clabel_10")


def solve_task_h53(state):
    """Merge CloudNine contacts, remove CloudNine delegates."""
    merge1 = find_merge(state, "merge_1")
    primary = find_contact(state, "Priya", "Sharma")
    secondary = find_contact(state, "Raj", "Kapoor")
    if not primary["secondaryEmail"] and secondary["email"]:
        primary["secondaryEmail"] = secondary["email"]
    if not primary["secondaryPhone"] and secondary["phone"]:
        primary["secondaryPhone"] = secondary["phone"]
    for lbl in secondary["labels"]:
        if lbl not in primary["labels"]:
            primary["labels"].append(lbl)
    if secondary["notes"] and secondary["notes"] not in primary["notes"]:
        primary["notes"] = (primary["notes"] + "\n" + secondary["notes"]
                            if primary["notes"] else secondary["notes"])
    state["contacts"] = [c for c in state["contacts"] if c["id"] != secondary["id"]]
    merge1["dismissed"] = True
    # Remove cloudnine.dev delegates
    state["delegates"] = [
        d for d in state["delegates"]
        if not d["email"].endswith("@cloudnine.dev")
    ]


def solve_task_h54(state):
    """Update David Kim secondary email and add Emergency."""
    david = find_contact(state, "David", "Kim")
    david["secondaryEmail"] = "david.kim@financeplus.com"
    if "clabel_10" not in david["labels"]:
        david["labels"].append("clabel_10")


def solve_task_h55(state):
    """Add VIP Clients to Sand Hill Rd contacts."""
    for c in state["contacts"]:
        if "Sand Hill Rd" in c.get("address", ""):
            if "clabel_4" not in c["labels"]:
                c["labels"].append("clabel_4")


def solve_task_h56(state):
    """Unstar Friends, then star unstarred VIP Clients."""
    for c in state["contacts"]:
        if "clabel_2" in c.get("labels", []):
            c["isStarred"] = False
    for c in state["contacts"]:
        if "clabel_4" in c.get("labels", []) and not c.get("isStarred"):
            c["isStarred"] = True


def solve_task_h57(state):
    """Delete Design contacts, dismiss merges, delete auto-saved from Design domains."""
    design_domains = ["designhub.com", "eurodesign.fr"]
    state["contacts"] = [
        c for c in state["contacts"]
        if "Design" not in c.get("company", "")
    ]
    # Dismiss merge_2 (EuroDesign)
    merge2 = find_merge(state, "merge_2")
    merge2["dismissed"] = True
    # Delete auto-saved from Design domains
    state["otherContacts"] = [
        oc for oc in state["otherContacts"]
        if not any(oc["email"].endswith(f"@{d}") for d in design_domains)
    ]


def solve_task_h58(state):
    """Phone visibility contacts_only, delegate notifs off, remove Family delegate."""
    state["accountSettings"]["privacySettings"]["showPhone"] = "contacts_only"
    state["accountSettings"]["notificationSettings"]["delegateActivity"] = False
    # Laura Johnson-Martinez has Family label
    state["delegates"] = [
        d for d in state["delegates"]
        if d["email"] != "laura.jm@gmail.com"
    ]


def solve_task_h59(state):
    """Create Inner Circle for starred+Friends, unstar Friends without Work."""
    nid = next_label_id(state)
    label_id = f"clabel_{nid}"
    state["contactLabels"].append({
        "id": label_id, "name": "Inner Circle",
        "color": "#E91E63", "contactCount": 0
    })
    for c in state["contacts"]:
        if c.get("isStarred") and "clabel_2" in c.get("labels", []):
            if label_id not in c["labels"]:
                c["labels"].append(label_id)
    for c in state["contacts"]:
        if "clabel_2" in c.get("labels", []) and "clabel_3" not in c.get("labels", []):
            c["isStarred"] = False


def solve_task_h60(state):
    """Five settings changes across multiple tabs."""
    state["accountSettings"]["notificationSettings"]["contactChanges"] = True
    state["accountSettings"]["notificationSettings"]["securityAlerts"] = False
    state["accountSettings"]["loginSettings"]["twoFactorMethod"] = "sms"
    state["accountSettings"]["contactsSortBy"] = "email"
    state["accountSettings"]["syncSettings"]["emailSync"] = False


# ── hardening round 3 solve functions ────────────────────────────────

def solve_task_h61(state):
    """Find 'vendor agreements and NDAs' contact, change company, add VIP Clients."""
    c = find_contact(state, "James", "O'Brien")
    c["company"] = "Morrison Legal Group"
    if "clabel_4" not in c["labels"]:
        c["labels"].append("clabel_4")


def solve_task_h62(state):
    """Most recently added delegate → update contact job title."""
    # Priya Sharma added 2026-03-05 (most recent)
    c = find_contact(state, "Priya", "Sharma")
    c["jobTitle"] = "Principal Engineer"


def solve_task_h63(state):
    """Find 'spare key' contact, star, add Family, change phone."""
    c = find_contact(state, "Ben", "Walker")
    c["isStarred"] = True
    if "clabel_1" not in c["labels"]:
        c["labels"].append("clabel_1")
    c["phone"] = "+1 (415) 555-9911"


def solve_task_h64(state):
    """Add VIP Clients to all July birthday contacts."""
    july_contacts = [
        ("David", "Kim"),
        ("Kevin", "Zhao"),
        ("Patricia", "Wong-Anderson"),
        ("Jake", "Morrison"),
    ]
    for first, last in july_contacts:
        c = find_contact(state, first, last)
        if "clabel_4" not in c["labels"]:
            c["labels"].append("clabel_4")


def solve_task_h65(state):
    """Recovery email = mother's email, recovery phone = father's phone."""
    state["currentUser"]["recoveryEmail"] = "margaret.johnson@gmail.com"
    state["currentUser"]["recoveryPhone"] = "+1 (916) 555-2602"


def solve_task_h66(state):
    """Find 'book club co-organizer', remove Neighbors, add VIP Clients."""
    c = find_contact(state, "Samantha", "Lee")
    c["labels"] = [lid for lid in c["labels"] if lid != "clabel_7"]
    if "clabel_4" not in c["labels"]:
        c["labels"].append("clabel_4")


def solve_task_h67(state):
    """Add VIP Clients to all contacts with 'Director' in job title."""
    director_contacts = [
        ("Marcus", "Williams"),
        ("Ana", "Gutierrez"),
        ("Sophie", "Laurent"),
        ("Jennifer", "Wu"),
        ("Rachel", "Foster"),
    ]
    for first, last in director_contacts:
        c = find_contact(state, first, last)
        if "clabel_4" not in c["labels"]:
            c["labels"].append("clabel_4")


def solve_task_h68(state):
    """Find 'office renovation' contact, star, add Friends and VIP Clients."""
    c = find_contact(state, "Daniel", "Thompson")
    c["isStarred"] = True
    if "clabel_2" not in c["labels"]:
        c["labels"].append("clabel_2")
    if "clabel_4" not in c["labels"]:
        c["labels"].append("clabel_4")


def solve_task_h69(state):
    """VIP Clients: starred → add Emergency, unstarred → star."""
    for c in state["contacts"]:
        if "clabel_4" in c.get("labels", []):
            if c.get("isStarred"):
                if "clabel_10" not in c["labels"]:
                    c["labels"].append("clabel_10")
            else:
                c["isStarred"] = True


def solve_task_h70(state):
    """Delete auto-saved contacts from best friend's company (Stripe)."""
    # Jake Morrison = best friend from college, company = Stripe
    # Auto-saved Stripe: no-reply@stripe.com
    state["otherContacts"] = [
        oc for oc in state["otherContacts"]
        if oc["email"] != "no-reply@stripe.com"
    ]


def solve_task_h71(state):
    """Find @cs.stanford.edu secondary email contact, update title, add VIP."""
    c = find_contact(state, "Robert", "Singh")
    c["jobTitle"] = "Distinguished Professor"
    if "clabel_4" not in c["labels"]:
        c["labels"].append("clabel_4")


def solve_task_h72(state):
    """Star Head of People Ops, unstar Eng Manager at TechCorp."""
    find_contact(state, "Patricia", "Wong-Anderson")["isStarred"] = True
    find_contact(state, "Maya", "Patel")["isStarred"] = False


def solve_task_h73(state):
    """Move most recently saved person (Jason Blake) to main contacts with fields."""
    other = find_other_contact(state, "jason.blake@salesforce.com")
    nid = next_contact_id(state)
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": other.get("firstName", ""),
        "lastName": other.get("lastName", ""),
        "email": other["email"], "phone": "", "company": "Salesforce",
        "jobTitle": "Account Executive", "address": "", "secondaryEmail": "",
        "secondaryPhone": "", "birthday": "", "website": "",
        "notes": "", "labels": ["clabel_3"], "isStarred": False,
        "avatarColor": "#EA4335",
        "createdAt": NOW, "updatedAt": NOW, "source": "auto-promoted"
    })
    state["otherContacts"] = [
        oc for oc in state["otherContacts"]
        if oc["email"] != "jason.blake@salesforce.com"
    ]


def solve_task_h74(state):
    """Trainer and instructor: remove Gym Buddies, add Friends."""
    for name in [("Hannah", "Brooks"), ("Diana", "Castillo")]:
        c = find_contact(state, name[0], name[1])
        c["labels"] = [lid for lid in c["labels"] if lid != "clabel_5"]
        if "clabel_2" not in c["labels"]:
            c["labels"].append("clabel_2")


def solve_task_h75(state):
    """Profile phone = FitnessFirst contact's phone, auto-save off."""
    state["currentUser"]["phone"] = "+1 (415) 555-1720"
    state["accountSettings"]["autoSaveContacts"] = False


def solve_task_h76(state):
    """Stanford contact: remove College Alumni, add Work and VIP Clients."""
    c = find_contact(state, "Robert", "Singh")
    c["labels"] = [lid for lid in c["labels"] if lid != "clabel_6"]
    if "clabel_3" not in c["labels"]:
        c["labels"].append("clabel_3")
    if "clabel_4" not in c["labels"]:
        c["labels"].append("clabel_4")


def solve_task_h77(state):
    """Create Hiro Tanaka with Yuki Tanaka's labels."""
    yuki = find_contact(state, "Yuki", "Tanaka")
    nid = next_contact_id(state)
    state["contacts"].append({
        "id": f"contact_{nid:02d}",
        "firstName": "Hiro", "lastName": "Tanaka",
        "email": "hiro.tanaka@gmail.com", "phone": "",
        "company": "", "jobTitle": "", "address": "",
        "secondaryEmail": "", "secondaryPhone": "", "birthday": "",
        "website": "", "notes": "", "labels": list(yuki["labels"]),
        "isStarred": False, "avatarColor": "#EA4335",
        "createdAt": NOW, "updatedAt": NOW, "source": "manual"
    })


def solve_task_h78(state):
    """Find 'AWS re:Invent 2024' contact, add College Alumni, update address."""
    c = find_contact(state, "Sarah", "Chen")
    if "clabel_6" not in c["labels"]:
        c["labels"].append("clabel_6")
    c["address"] = "500 Tech Park Dr, Menlo Park, CA 94025"


def solve_task_h79(state):
    """Find 'property search in East Bay' contact, add as delegate, add VIP Clients."""
    c = find_contact(state, "Tom", "Bradley")
    if "clabel_4" not in c["labels"]:
        c["labels"].append("clabel_4")
    nid = next_delegate_id(state)
    state["delegates"].append({
        "id": f"delegate_{nid}",
        "email": "tom.bradley@realtyhome.com",
        "name": "Tom Bradley",
        "status": "pending",
        "addedAt": NOW,
        "activatedAt": None,
        "permissions": {
            "readEmail": True, "sendEmail": True, "deleteEmail": True,
            "manageChat": False, "changePassword": False
        }
    })


def solve_task_h80(state):
    """Unstar contacts with exactly 1 label, star those with 3+ labels."""
    for c in state["contacts"]:
        label_count = len(c.get("labels", []))
        if label_count == 1 and c.get("isStarred"):
            c["isStarred"] = False
        elif label_count >= 3 and not c.get("isStarred"):
            c["isStarred"] = True


# ── solver registry ──────────────────────────────────────────────────

SOLVERS = {}
for _i in range(1, 21):
    SOLVERS[f"task_e{_i}"] = globals()[f"solve_task_e{_i}"]
    SOLVERS[f"task_m{_i}"] = globals()[f"solve_task_m{_i}"]
    SOLVERS[f"task_h{_i}"] = globals()[f"solve_task_h{_i}"]
for _i in range(21, 81):
    SOLVERS[f"task_h{_i}"] = globals()[f"solve_task_h{_i}"]


# ── server management ────────────────────────────────────────────────

def generate_seed_state():
    """Use Node.js to evaluate data.js and produce the seed state JSON."""
    data_js = str(APP_DIR / "js" / "data.js")
    result = subprocess.run(
        ["node", "-e", _SEED_STATE_JS, data_js],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate seed state:\n{result.stderr}")
    return json.loads(result.stdout)


def seed_server(server_url, seed_state):
    """PUT the seed state to establish the baseline."""
    resp = requests.put(
        f"{server_url}/api/state",
        json=seed_state,
        headers={"Content-Type": "application/json"},
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to seed server: HTTP {resp.status_code}")


def find_free_port(start=9000):
    port = start
    while port < start + 200:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"No free port found in range {start}-{start+200}")


def start_server(port):
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
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ── task runner ──────────────────────────────────────────────────────

def load_tasks():
    with open(TASKS_FILE) as f:
        return json.load(f)


def load_verifier(verify_path):
    full_path = APP_DIR / verify_path
    spec = importlib.util.spec_from_file_location("verifier", str(full_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


def run_single_task(task, server_url):
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
    parser = argparse.ArgumentParser(description="Gmail Accounts & Contacts real-task sanity check")
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
