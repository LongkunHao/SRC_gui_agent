import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check secondary timezone is set to none/empty/null
    settings = state.get("settings", {})
    secondary_tz = settings.get("secondaryTimezone")

    # Accept None, empty string, "none", "None", or missing key
    if secondary_tz is None or secondary_tz == "" or str(secondary_tz).lower() == "none":
        return True, "Secondary timezone has been successfully set to none."
    else:
        return False, f"Secondary timezone is '{secondary_tz}', expected it to be none/empty/null."
