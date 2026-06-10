import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    enabled = state.get("settings", {}).get("autoDrafts", {}).get("enabled")
    if enabled is False:
        return True, "Auto drafts are disabled."
    return False, f"Auto drafts are not disabled (enabled={enabled!r})."
