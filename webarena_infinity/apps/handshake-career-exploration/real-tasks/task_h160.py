"""
Task: Answer the Q&A question about whether to accept a return offer with
your advice about weighing options. Then find the employer whose affiliated
companies include 'Instagram' and RSVP to their upcoming virtual event.

Discovery: Return offer Q&A → qa_09.
Instagram affiliate → Meta (emp_07).
Meta upcoming virtual event: evt_02 (AI/ML Careers, Virtual Session).

Verify:
(1) qa_09 has a new answer
(2) evt_02 rsvped
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    questions = state.get("qaQuestions", [])
    events = state.get("events", [])

    # Check 1: qa_09 has new answer
    qa_09 = next((q for q in questions if q.get("id") == "qa_09"), None)
    if qa_09 is None:
        errors.append("qa_09 not found.")
    else:
        seed_ans_ids = {"ans_12"}
        new_answers = [
            a for a in qa_09.get("answers", [])
            if a.get("id") not in seed_ans_ids
        ]
        if not new_answers:
            errors.append("No new answer on qa_09.")

    # Check 2: evt_02 RSVPed
    evt_02 = next((e for e in events if e.get("id") == "evt_02"), None)
    if evt_02 is None:
        errors.append("evt_02 not found.")
    elif not evt_02.get("rsvped"):
        errors.append("evt_02 (Meta AI/ML Virtual Session) not RSVP'd.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Return offer Q&A answered. "
        "Meta event RSVP'd (Instagram affiliate discovery)."
    )
