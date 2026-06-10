import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify reply to thirst/urination patient + High Risk tag added."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Raymond Copeland (pat_35) wrote about increased thirst and urination
    pat = None
    for p in state.get("patients", []):
        if p.get("firstName") == "Raymond" and p.get("lastName") == "Copeland":
            pat = p
            break

    if pat is None:
        return False, "Raymond Copeland not found in patients"

    # Check High Risk tag
    if "High Risk" not in pat.get("tags", []):
        return False, f"Raymond Copeland is missing 'High Risk' tag. Current tags: {pat.get('tags', [])}"

    # Check reply exists in conv_34
    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}
    has_reply = False
    for ltr in state.get("patientLetters", []):
        if (ltr.get("conversationId") == "conv_34"
                and ltr.get("direction") == "to_patient"
                and ltr.get("id") not in seed_letter_ids
                and not ltr.get("isDraft", False)):
            has_reply = True
            break

    if not has_reply:
        return False, "No reply found in Raymond Copeland's conversation (conv_34)"

    return True, "Replied to Raymond Copeland about A1C test and added 'High Risk' tag"
