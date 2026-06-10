import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    merge_suggestions = state.get("mergeSuggestions", [])
    merge_2 = None
    for ms in merge_suggestions:
        if ms.get("id") == "merge_2":
            merge_2 = ms
            break

    if merge_2 is None:
        return False, "Merge suggestion 'merge_2' not found."

    if not merge_2.get("dismissed"):
        return False, f"Merge suggestion 'merge_2' is not dismissed. dismissed={merge_2.get('dismissed')}."

    return True, "Merge suggestion 'merge_2' (Sophie Laurent + Elena Volkov) has dismissed=True."
