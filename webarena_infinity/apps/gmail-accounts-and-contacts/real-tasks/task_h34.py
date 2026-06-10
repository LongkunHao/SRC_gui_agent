# Task: Security key 2FA, disable auto sign-in and remember password, all visibility to contacts_only.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    settings = state.get("accountSettings", {})
    login = settings.get("loginSettings", {})
    privacy = settings.get("privacySettings", {})

    # Login settings checks
    if login.get("twoFactorMethod") != "security_key":
        errors.append(
            f"2FA method is '{login.get('twoFactorMethod')}' instead of 'security_key'"
        )
    if login.get("autoSignIn") is not False:
        errors.append("Auto sign-in should be disabled")
    if login.get("rememberPassword") is not False:
        errors.append("Remember password should be disabled")

    # Privacy settings checks — all should be contacts_only
    for field, label in [
        ("showProfilePhoto", "Profile photo visibility"),
        ("showEmail", "Email visibility"),
        ("showPhone", "Phone visibility"),
    ]:
        val = privacy.get(field)
        if val != "contacts_only":
            errors.append(f"{label} is '{val}' instead of 'contacts_only'")

    if errors:
        return False, "; ".join(errors)
    return True, "Security settings configured: security key 2FA, no auto-login, contacts-only visibility."
