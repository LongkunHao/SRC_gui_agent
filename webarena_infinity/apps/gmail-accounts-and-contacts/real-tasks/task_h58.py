# Task: Phone visibility to contacts_only, disable delegate notifications, remove Family delegate.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    settings = state.get("accountSettings", {})
    delegates = state.get("delegates", [])

    # Phone visibility should be contacts_only
    ps = settings.get("privacySettings", {})
    if ps.get("showPhone") != "contacts_only":
        errors.append(
            f"Phone visibility is '{ps.get('showPhone')}' "
            "instead of 'contacts_only'"
        )

    # Delegate activity notifications should be off
    ns = settings.get("notificationSettings", {})
    if ns.get("delegateActivity") is not False:
        errors.append("Delegate activity notifications should be disabled")

    # Laura Johnson-Martinez (Family label) should be removed as delegate
    for d in delegates:
        if d.get("email") == "laura.jm@gmail.com":
            errors.append(
                "Laura Johnson-Martinez should be removed as delegate "
                "(her contact has Family label)"
            )

    # Other delegates should remain
    for email in ["maya.patel@techcorp.io", "priya.sharma@cloudnine.dev",
                   "jake.morrison@gmail.com"]:
        found = any(d.get("email") == email for d in delegates)
        if not found:
            errors.append(f"Delegate '{email}' should still exist")

    if errors:
        return False, "; ".join(errors)
    return True, "Phone visibility updated, delegate notifications off, Family delegate removed."
