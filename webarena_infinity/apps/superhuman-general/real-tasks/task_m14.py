import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find the "Meeting Follow-up" snippet
    target_snippet = None
    for snippet in state.get("snippets", []):
        if snippet.get("name") == "Meeting Follow-up":
            target_snippet = snippet
            break

    if not target_snippet:
        return False, "Could not find snippet 'Meeting Follow-up' in state."

    # Check that isShared is True
    if target_snippet.get("isShared") == True:
        return True, "Snippet 'Meeting Follow-up' is shared with the team."
    else:
        return False, f"Snippet 'Meeting Follow-up' is not shared. isShared: {target_snippet.get('isShared')}"
