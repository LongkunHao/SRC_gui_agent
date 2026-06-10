import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify reply sent in conv_22 (Aisha Patel's ankle swelling conversation)
    and 'High Risk' tag added to pat_20."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    # Check for 'High Risk' tag on pat_20 (Aisha Patel)
    pat_20 = None
    for pat in state.get("patients", []):
        if pat.get("id") == "pat_20":
            pat_20 = pat
            break

    if pat_20 is None:
        return False, "Patient pat_20 (Aisha Patel) not found"

    if "High Risk" not in pat_20.get("tags", []):
        return False, (
            f"Aisha Patel (pat_20) is missing 'High Risk' tag. "
            f"Current tags: {pat_20.get('tags', [])}"
        )

    # Check for new reply in conv_22
    seed_letter_ids = {f"ltr_{i}" for i in range(1, 48)}

    has_reply = False
    for ltr in state.get("patientLetters", []):
        if (ltr.get("conversationId") == "conv_22"
                and ltr.get("direction") == "to_patient"
                and ltr.get("id") not in seed_letter_ids
                and not ltr.get("isDraft", False)):
            has_reply = True
            break

    if not has_reply:
        return False, (
            "No new reply found in conv_22 (Aisha Patel's ankle swelling conversation)"
        )

    return True, (
        "Reply sent in conv_22 about ankle swelling and 'High Risk' tag added to Aisha Patel"
    )
