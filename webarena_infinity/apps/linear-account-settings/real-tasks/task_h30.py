# Task: Revoke non-current desktop sessions, disable desktop notifications, turn off desktop app settings.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # No non-current desktop sessions should remain
    sessions = state.get("sessions", [])
    bad_sessions = [s for s in sessions
                    if s.get("deviceType") == "desktop" and not s.get("isCurrent")]
    if bad_sessions:
        names = [s.get("deviceName") for s in bad_sessions]
        failures.append(f"Non-current desktop sessions still present: {names}")

    # Non-desktop sessions (mobile, tablet) should still exist
    non_desktop = [s for s in sessions if s.get("deviceType") != "desktop"]
    if len(non_desktop) == 0:
        failures.append("Non-desktop sessions were incorrectly removed")

    # Desktop notification channel disabled
    desktop_notif = state.get("notificationSettings", {}).get("desktop", {})
    if desktop_notif.get("enabled") is not False:
        failures.append("Desktop notification channel should be disabled")

    # All desktop app preferences off
    prefs = state.get("preferences", {})
    if prefs.get("openInDesktopApp") is not False:
        failures.append("openInDesktopApp should be false")
    if prefs.get("desktopNotificationBadge") is not False:
        failures.append("desktopNotificationBadge should be false")
    if prefs.get("enableSpellCheck") is not False:
        failures.append("enableSpellCheck should be false")

    if failures:
        return False, "; ".join(failures)
    return True, "Desktop sessions revoked, desktop notifications disabled, desktop app settings off."
