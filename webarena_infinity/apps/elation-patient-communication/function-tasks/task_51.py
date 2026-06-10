import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify waiting room audio notification is disabled."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    video_settings = state.get("practiceSettings", {}).get("videoSettings", {})
    audio_notification = video_settings.get("waitingRoomAudioNotification")

    if audio_notification is not False:
        return False, f"videoSettings.waitingRoomAudioNotification is {audio_notification}, expected False"

    return True, "Waiting room audio notification is correctly disabled"
