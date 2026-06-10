import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Starred emails that were originally in Done should now be un-archived
    # Seed starred+done emails: ids 80, 81, 82
    target_subjects = [
        ("FY2026 Budget Summary", "priya.sharma@acmecorp.com"),
        ("Company Vision & Strategy 2026-2028", "patrick.oneil@acmecorp.com"),
        ("Customer Success Metrics - February", "sarah.chen@acmecorp.com"),
    ]

    still_done = []
    for subj, sender in target_subjects:
        for e in state.get("emails", []):
            if e["subject"] == subj and e["from"]["email"] == sender:
                if e.get("isDone", False):
                    still_done.append(f"'{subj}'")
                if not e.get("isStarred", False):
                    return False, f"Email '{subj}' lost its star during the operation."
                break
        else:
            return False, f"Email '{subj}' from {sender} not found."

    if still_done:
        return False, f"{len(still_done)} starred email(s) still in Done: {', '.join(still_done)}"

    return True, "All 3 starred emails moved from Done back to inbox."
