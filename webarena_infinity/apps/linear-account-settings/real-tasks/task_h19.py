# Task: Turn off all desktop application settings: open in desktop app,
# notification badge, and spell check.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    prefs = state.get("preferences", {})

    checks = [
        (prefs.get("openInDesktopApp") == False, f"openInDesktopApp: expected False, got {prefs.get('openInDesktopApp')}"),
        (prefs.get("desktopNotificationBadge") == False, f"desktopNotificationBadge: expected False, got {prefs.get('desktopNotificationBadge')}"),
        (prefs.get("enableSpellCheck") == False, f"enableSpellCheck: expected False, got {prefs.get('enableSpellCheck')}"),
    ]

    failures = [msg for ok, msg in checks if not ok]
    if failures:
        return False, "; ".join(failures)
    return True, "All desktop application settings turned off."
