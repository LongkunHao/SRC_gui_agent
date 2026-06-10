import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    provider = state.get("settings", {}).get("meetingLink", {}).get("provider")
    if provider == "google-meet":
        return True, "Meeting link provider is set to Google Meet."
    return False, f"Meeting link provider is not Google Meet (provider={provider!r})."
