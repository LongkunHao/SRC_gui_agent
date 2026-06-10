# Task: Switch to high-contrast light theme, set font to small, enable pointer cursor, turn off emoticon conversion.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    prefs = state.get("preferences", {})

    checks = [
        (prefs.get("interfaceTheme") == "Light - Contrast", f"interfaceTheme is '{prefs.get('interfaceTheme')}', expected 'Light - Contrast'"),
        (prefs.get("fontSize") == "Small", f"fontSize is '{prefs.get('fontSize')}', expected 'Small'"),
        (prefs.get("usePointerCursor") is True, f"usePointerCursor is {prefs.get('usePointerCursor')}, expected True"),
        (prefs.get("convertTextEmojis") is False, f"convertTextEmojis is {prefs.get('convertTextEmojis')}, expected False"),
    ]
    for passed, msg in checks:
        if not passed:
            return False, msg
    return True, "All preference changes verified."
