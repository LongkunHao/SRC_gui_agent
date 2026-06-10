import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify screen sharing for patients is disabled."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    video_settings = state.get("practiceSettings", {}).get("videoSettings", {})
    screen_sharing = video_settings.get("screenSharingPatients")

    if screen_sharing is not False:
        return False, f"videoSettings.screenSharingPatients is {screen_sharing}, expected False"

    return True, "Screen sharing for patients is correctly disabled"
