import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    snippets = state.get("snippets", [])

    # Check that "Thank You" no longer exists (was renamed)
    old_exists = any(s["name"] == "Thank You" for s in snippets)

    # Check that "Client Thank You" exists and is shared
    new_snippet = None
    for s in snippets:
        if s["name"] == "Client Thank You":
            new_snippet = s
            break

    if not new_snippet and not old_exists:
        return False, "Neither 'Thank You' nor 'Client Thank You' snippet found."
    if not new_snippet:
        return False, "Snippet 'Client Thank You' not found. 'Thank You' still exists — was it renamed?"

    errors = []
    if old_exists:
        errors.append("Original 'Thank You' snippet still exists alongside 'Client Thank You'.")
    if not new_snippet.get("isShared"):
        errors.append("'Client Thank You' snippet is not shared with the team.")

    if errors:
        return False, " ".join(errors)

    return True, "Snippet renamed to 'Client Thank You' and shared with the team."
