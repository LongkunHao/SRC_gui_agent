import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    snippets = state.get("snippets", [])
    snippet_names = [s.get("name", "") for s in snippets]

    # Check "Decline Politely" is deleted
    if "Decline Politely" in snippet_names:
        return False, "Snippet 'Decline Politely' still exists (should be deleted)."

    # Check "Quick Check-in" is deleted
    if "Quick Check-in" in snippet_names:
        return False, "Snippet 'Quick Check-in' still exists (should be deleted)."

    # Find "Introduction" snippet and check isShared==false
    intro_snippet = None
    for s in snippets:
        if s.get("name") == "Introduction":
            intro_snippet = s
            break
    if not intro_snippet:
        return False, "Snippet 'Introduction' not found (it should still exist but with sharing disabled)."
    if intro_snippet.get("isShared") is not False:
        return False, f"Snippet 'Introduction' isShared is {intro_snippet.get('isShared')}, expected false."

    return True, "'Decline Politely' and 'Quick Check-in' deleted, 'Introduction' sharing disabled."
