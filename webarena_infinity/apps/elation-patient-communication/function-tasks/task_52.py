import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify video chat mode changed to 'host_only'."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    video_settings = state.get("practiceSettings", {}).get("videoSettings", {})
    chat_mode = video_settings.get("chatMode")

    if chat_mode != "host_only":
        return False, f"videoSettings.chatMode is '{chat_mode}', expected 'host_only'"

    return True, "Video chat mode correctly changed to 'host_only'"
