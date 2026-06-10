# Task: Multiple settings changes across different tabs.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    settings = state.get("accountSettings", {})

    # Contact changes notifications should be enabled
    ns = settings.get("notificationSettings", {})
    if ns.get("contactChanges") is not True:
        errors.append("Contact changes notifications should be enabled")

    # Security alerts should be disabled
    if ns.get("securityAlerts") is not False:
        errors.append("Security alerts should be disabled")

    # 2FA method should be SMS
    ls = settings.get("loginSettings", {})
    if ls.get("twoFactorMethod") != "sms":
        errors.append(
            f"2FA method is '{ls.get('twoFactorMethod')}' instead of 'sms'"
        )

    # Contact sort should be by email
    if settings.get("contactsSortBy") != "email":
        errors.append(
            f"Contact sort is '{settings.get('contactsSortBy')}' instead of 'email'"
        )

    # Email sync should be off
    ss = settings.get("syncSettings", {})
    if ss.get("emailSync") is not False:
        errors.append("Email sync should be disabled")

    if errors:
        return False, "; ".join(errors)
    return True, "All five settings updated correctly."
