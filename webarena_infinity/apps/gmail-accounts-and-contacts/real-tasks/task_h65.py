# Task: Set recovery email to mother's email, recovery phone to father's phone.
import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    errors = []

    current_user = state.get("currentUser", {})

    # Mother = Margaret Johnson, email = margaret.johnson@gmail.com
    if current_user.get("recoveryEmail") != "margaret.johnson@gmail.com":
        errors.append(
            f"Recovery email is '{current_user.get('recoveryEmail')}' "
            f"instead of 'margaret.johnson@gmail.com'"
        )

    # Father = Richard Johnson, phone = +1 (916) 555-2602
    if current_user.get("recoveryPhone") != "+1 (916) 555-2602":
        errors.append(
            f"Recovery phone is '{current_user.get('recoveryPhone')}' "
            f"instead of '+1 (916) 555-2602'"
        )

    if errors:
        return False, "; ".join(errors)
    return True, "Recovery email and phone updated to match parents' contact info."
