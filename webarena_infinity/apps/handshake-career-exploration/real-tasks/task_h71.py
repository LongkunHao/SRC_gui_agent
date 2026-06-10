"""
Task: RSVP to every upcoming event hosted by an employer (not the career center),
and save each of those employers' active jobs you haven't saved yet.

Employer-hosted upcoming events:
- evt_01: emp_04 (McKinsey) -> job_05
- evt_02: emp_07 (Meta) -> job_07 (saved), job_26
- evt_04: emp_01 (Google) -> job_01, job_02, job_22
- evt_06: emp_15 (Anthropic) -> job_12 (saved), job_29
- evt_08: emp_02 (JPMorgan) -> job_27 (job_03 closed)
- evt_10: emp_19 (Salesforce) -> job_17, job_30

Career center events (skip): evt_03, evt_05, evt_07, evt_09

Verify:
(1) All 6 employer events RSVP'd.
(2) All unsaved active jobs from those employers saved.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: All employer-hosted upcoming events RSVP'd
    events = state.get("events", [])
    required_events = {
        "evt_01": "McKinsey Campus Presentation",
        "evt_02": "Meta AI/ML Info Session",
        "evt_04": "Google Tech Talk",
        "evt_06": "Anthropic Research Talk",
        "evt_08": "JPMorgan Markets & Trading Panel",
        "evt_10": "Salesforce Futureforce",
    }
    for evt_id, name in required_events.items():
        evt = next((e for e in events if e.get("id") == evt_id), None)
        if evt is None:
            errors.append(f"{evt_id} ({name}) not found.")
        elif evt.get("rsvped") != True:
            errors.append(f"{evt_id} ({name}) not RSVP'd.")

    # Check 2: All unsaved active jobs from those employers saved
    saved = state.get("currentUser", {}).get("savedJobIds", [])
    required_jobs = {
        "job_01": "Google SWE Intern",
        "job_02": "Google APM Intern",
        "job_05": "McKinsey BA Intern",
        "job_17": "Salesforce SWE New Grad",
        "job_22": "Google UX Design Intern",
        "job_26": "Meta Product Design Intern",
        "job_27": "JPMorgan Quant Research",
        "job_29": "Anthropic Policy Research Intern",
        "job_30": "Salesforce Marketing Analyst Intern",
    }
    missing_jobs = []
    for job_id, title in required_jobs.items():
        if job_id not in saved:
            missing_jobs.append(f"{title} ({job_id})")
    if missing_jobs:
        errors.append(
            f"Active jobs from event employers not saved: {missing_jobs}. "
            f"Current savedJobIds: {saved}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All 6 employer-hosted events RSVP'd and their active unsaved jobs saved "
        "(9 additional jobs)."
    )
