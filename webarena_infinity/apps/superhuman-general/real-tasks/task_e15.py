import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    enabled = state.get("settings", {}).get("autoArchive", {}).get("enabled")
    if enabled is False:
        return True, "Auto archive is disabled."
    return False, f"Auto archive is not disabled (enabled={enabled!r})."
