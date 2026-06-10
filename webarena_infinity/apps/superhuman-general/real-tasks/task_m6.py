import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find snippet with name "Project Update"
    target_snippet = None
    for snippet in state.get("snippets", []):
        if snippet.get("name") == "Project Update":
            target_snippet = snippet
            break

    if not target_snippet:
        return False, "Could not find a snippet named 'Project Update' in state."

    # Check body contains "latest update on"
    body = target_snippet.get("body", "")
    if "latest update on" in body.lower():
        return True, f"Snippet 'Project Update' exists with correct body content."
    else:
        return False, f"Snippet 'Project Update' exists but body does not contain 'latest update on'. Body: {body}"
