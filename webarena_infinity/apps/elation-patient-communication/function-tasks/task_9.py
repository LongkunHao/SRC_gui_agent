import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify draft letter ltr_35 (to Martha Reeves-Whitfield, pat_36) has been deleted."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    letters = state.get("patientLetters", [])

    for l in letters:
        if l.get("id") == "ltr_35":
            return False, (
                f"Letter ltr_35 still exists in patientLetters "
                f"(subject: '{l.get('subject')}', isDraft: {l.get('isDraft')}). "
                f"Expected it to be deleted."
            )

    return True, "Draft letter ltr_35 (Martha Reeves-Whitfield) has been deleted"
