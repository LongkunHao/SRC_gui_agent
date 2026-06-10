"""
Task: RSVP to every upcoming in-person event hosted by an employer (not career center),
save at least one active job from each host.

Discovery: In-person employer events (upcoming): evt_01 (McKinsey emp_04), evt_04 (Google emp_01),
evt_08 (JPMorgan emp_02). McKinsey active jobs: job_05. Google: job_01, job_02, job_22.
JPMorgan: job_27.

Verify:
(1) evt_01.rsvped == True
(2) evt_04.rsvped == True
(3) evt_08.rsvped == True
(4) At least one of [job_05] in savedJobIds (McKinsey)
(5) At least one of [job_01, job_02, job_22] in savedJobIds (Google)
(6) At least one of [job_27] in savedJobIds (JPMorgan)
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check RSVP status for all three in-person employer events
    events = state.get("events", [])

    required_rsvps = {
        "evt_01": "McKinsey Case Competition Workshop",
        "evt_04": "Google Tech Talk: Future of AI",
        "evt_08": "JPMorgan Investment Banking Info Session",
    }

    for evt_id, evt_title in required_rsvps.items():
        evt = next((e for e in events if e.get("id") == evt_id), None)
        if evt is None:
            errors.append(f"Event {evt_id} ({evt_title}) not found in events.")
        elif evt.get("rsvped") is not True:
            errors.append(
                f"Event {evt_id} ({evt_title}) is not RSVP'd. "
                f"rsvped={evt.get('rsvped')}"
            )

    # Check saved jobs from each employer host
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    # McKinsey (emp_04) active jobs
    mckinsey_jobs = ["job_05"]
    if not any(j in saved_job_ids for j in mckinsey_jobs):
        errors.append(
            f"No McKinsey active job saved. Expected at least one of {mckinsey_jobs} "
            f"in savedJobIds. Current savedJobIds: {saved_job_ids}"
        )

    # Google (emp_01) active jobs
    google_jobs = ["job_01", "job_02", "job_22"]
    if not any(j in saved_job_ids for j in google_jobs):
        errors.append(
            f"No Google active job saved. Expected at least one of {google_jobs} "
            f"in savedJobIds. Current savedJobIds: {saved_job_ids}"
        )

    # JPMorgan (emp_02) active jobs
    jpmorgan_jobs = ["job_27"]
    if not any(j in saved_job_ids for j in jpmorgan_jobs):
        errors.append(
            f"No JPMorgan active job saved. Expected at least one of {jpmorgan_jobs} "
            f"in savedJobIds. Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All in-person employer events RSVP'd (evt_01, evt_04, evt_08) and "
        "at least one active job saved from each host employer (McKinsey, Google, JPMorgan)."
    )
