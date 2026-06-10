import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for snippet in state.get("snippets", []):
        if snippet.get("name") == "Out of Office":
            return False, "The 'Out of Office' snippet still exists."

    return True, "The 'Out of Office' snippet has been deleted."
