# Task: Invert every notification channel's enabled state; do not change types.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    ns = state.get("notificationSettings", {})
    failures = []

    # Seed: desktop=enabled, mobile=enabled, email=enabled, slack=disabled
    # After invert: desktop=disabled, mobile=disabled, email=disabled, slack=enabled
    expected_enabled = {
        "desktop": False,
        "mobile": False,
        "email": False,
        "slack": True
    }
    for channel, expected in expected_enabled.items():
        actual = ns.get(channel, {}).get("enabled")
        if actual != expected:
            failures.append(f"{channel}.enabled should be {expected}, got {actual}")

    # Notification types should remain unchanged from seed
    seed_types = {
        "desktop": {"issueAssigned": True, "issueStatusChanged": True, "issueCommented": True,
                     "issueMentioned": True, "projectUpdated": True, "cycleUpdated": False},
        "mobile": {"issueAssigned": True, "issueStatusChanged": True, "issueCommented": True,
                    "issueMentioned": True, "projectUpdated": False, "cycleUpdated": False},
        "email": {"issueAssigned": True, "issueStatusChanged": True, "issueCommented": False,
                   "issueMentioned": True, "projectUpdated": False, "cycleUpdated": False},
        "slack": {"issueAssigned": False, "issueStatusChanged": False, "issueCommented": False,
                   "issueMentioned": False, "projectUpdated": False, "cycleUpdated": False}
    }
    for channel, types in seed_types.items():
        ch = ns.get(channel, {})
        for key, val in types.items():
            if ch.get(key) != val:
                failures.append(f"{channel}.{key} should remain {val}, got {ch.get(key)}")

    if failures:
        return False, "; ".join(failures)
    return True, "All channel enabled states inverted; notification types unchanged."
