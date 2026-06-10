import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prof = next((t for t in state["brandingThemes"] if t["id"] == "theme_professional"), None)
    if not prof:
        return False, "Branding theme 'Professional Services' not found."

    if not prof["isDefault"]:
        return False, "Professional Services theme is not set as default."

    # Also check that Standard is no longer default
    std = next((t for t in state["brandingThemes"] if t["id"] == "theme_standard"), None)
    if std and std["isDefault"]:
        return False, "Standard theme is still set as default."

    return True, "Professional Services set as default branding theme."
