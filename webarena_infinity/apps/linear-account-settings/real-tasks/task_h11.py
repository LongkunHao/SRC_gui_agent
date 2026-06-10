# Task: Set up preferences for a minimal workspace: dark theme, small font, home view Inbox,
# turn off full names, disable emoticon conversion, turn off open in desktop app.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    prefs = state.get("preferences", {})

    checks = [
        (prefs.get("interfaceTheme") == "Dark", f"interfaceTheme: expected 'Dark', got '{prefs.get('interfaceTheme')}'"),
        (prefs.get("fontSize") == "Small", f"fontSize: expected 'Small', got '{prefs.get('fontSize')}'"),
        (prefs.get("defaultHomeView") == "Inbox", f"defaultHomeView: expected 'Inbox', got '{prefs.get('defaultHomeView')}'"),
        (prefs.get("displayFullNames") == False, f"displayFullNames: expected False, got {prefs.get('displayFullNames')}"),
        (prefs.get("convertTextEmojis") == False, f"convertTextEmojis: expected False, got {prefs.get('convertTextEmojis')}"),
        (prefs.get("openInDesktopApp") == False, f"openInDesktopApp: expected False, got {prefs.get('openInDesktopApp')}"),
    ]

    failures = [msg for ok, msg in checks if not ok]
    if failures:
        return False, "; ".join(failures)
    return True, "All minimal workspace preferences set correctly."
