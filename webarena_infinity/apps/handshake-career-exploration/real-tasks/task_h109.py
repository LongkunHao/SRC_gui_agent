"""
Task: A Stripe alumni mentioned learning about distributed systems.
Find their answer in Q&A and mark it helpful, then read Stripe's unread message.

Discovery: Stripe testimonial by Marcus Johnson mentions distributed systems.
Marcus Johnson answered qa_09 (ans_12). Stripe message: msg_06 (unread).

Verify:
(1) ans_12 helpful > 35 (seed)
(2) msg_06 isRead == True
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    questions = state.get("qaQuestions", [])
    qa_09 = next((q for q in questions if q.get("id") == "qa_09"), None)
    if qa_09 is None:
        errors.append("qa_09 not found.")
    else:
        ans_12 = next(
            (a for a in qa_09.get("answers", []) if a.get("id") == "ans_12"), None
        )
        if ans_12 is None:
            errors.append("ans_12 not found in qa_09.")
        elif ans_12.get("helpful", 0) <= 35:
            errors.append(
                f"ans_12 helpful not incremented. Expected > 35, got {ans_12.get('helpful')}"
            )

    messages = state.get("messages", [])
    msg_06 = next((m for m in messages if m.get("id") == "msg_06"), None)
    if msg_06 is None:
        errors.append("msg_06 not found.")
    elif not msg_06.get("isRead"):
        errors.append(f"msg_06 not read. isRead={msg_06.get('isRead')}")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Marcus Johnson identified from Stripe's distributed systems testimonial. "
        "His Q&A answer (ans_12) marked helpful and Stripe message (msg_06) read."
    )
