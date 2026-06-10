# Task: Switch to the high-contrast dark theme and make the font size small.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    prefs = state.get("preferences", {})
    theme = prefs.get("interfaceTheme", "")
    font_size = prefs.get("fontSize", "")
    errors = []
    if theme != "Dark - Contrast":
        errors.append(f"Expected interfaceTheme 'Dark - Contrast', got '{theme}'")
    if font_size != "Small":
        errors.append(f"Expected fontSize 'Small', got '{font_size}'")
    if errors:
        return False, "; ".join(errors)
    return True, "Theme and font size updated correctly."
