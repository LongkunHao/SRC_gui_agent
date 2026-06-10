import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find snippet "NDA Request"
    nda_snippet = None
    for s in state.get("snippets", []):
        if s.get("name") == "NDA Request":
            nda_snippet = s
            break
    if not nda_snippet:
        return False, "Snippet 'NDA Request' not found."

    # Check body contains expected content
    body = nda_snippet.get("body", "")
    body_lower = body.lower()
    if "nda" not in body_lower:
        return False, f"Snippet body does not contain 'NDA'. Body: '{body[:100]}...'"
    if "review and sign" not in body_lower:
        return False, f"Snippet body does not contain 'review and sign'. Body: '{body[:100]}...'"

    # Check isShared
    if nda_snippet.get("isShared") is not True:
        return False, f"Snippet 'NDA Request' isShared is {nda_snippet.get('isShared')}, expected true."

    return True, "Snippet 'NDA Request' created with correct body and shared with team."
