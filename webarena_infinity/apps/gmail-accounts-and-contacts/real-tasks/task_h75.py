# Task: Update profile phone to FitnessFirst contact's phone, turn off auto-save.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    # Hannah Brooks at FitnessFirst: phone = '+1 (415) 555-1720'
    current_user = state.get("currentUser", {})
    if current_user.get("phone") != "+1 (415) 555-1720":
        errors.append(
            f"Profile phone is '{current_user.get('phone')}' "
            f"instead of '+1 (415) 555-1720'"
        )

    if state.get("accountSettings", {}).get("autoSaveContacts") is not False:
        errors.append("Auto-save contacts should be turned off")

    if errors:
        return False, "; ".join(errors)
    return True, "Profile phone updated and auto-save contacts disabled."
