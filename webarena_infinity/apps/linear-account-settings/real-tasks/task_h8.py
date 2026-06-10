# Task: Unsubscribe from all communication notifications and disable email channel.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    notif = state.get("notificationSettings", {})

    checks = [
        (notif.get("receiveChangelogs") is False, f"receiveChangelogs is {notif.get('receiveChangelogs')}, expected False"),
        (notif.get("receiveDpaUpdates") is False, f"receiveDpaUpdates is {notif.get('receiveDpaUpdates')}, expected False"),
        (notif.get("receiveProductUpdates") is False, f"receiveProductUpdates is {notif.get('receiveProductUpdates')}, expected False"),
        (notif.get("email", {}).get("enabled") is False, f"email.enabled is {notif.get('email', {}).get('enabled')}, expected False"),
    ]
    for passed, msg in checks:
        if not passed:
            return False, msg
    return True, "Communication notifications and email channel disabled."
