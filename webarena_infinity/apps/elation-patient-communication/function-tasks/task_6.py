import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify conversation conv_22 (Aisha Patel) is ended."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    letters = state.get("patientLetters", [])

    conv_22_letters = [l for l in letters if l.get("conversationId") == "conv_22"]

    if not conv_22_letters:
        return False, "No letters found for conversation conv_22"

    for letter in conv_22_letters:
        conv_state = letter.get("conversationState")
        if conv_state != "ended":
            return False, (
                f"Letter {letter.get('id')} in conv_22 has conversationState '{conv_state}', "
                f"expected 'ended'"
            )

    return True, f"Conversation conv_22 (Aisha Patel) is ended ({len(conv_22_letters)} letters all have state 'ended')"
