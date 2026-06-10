# Task: Change name to 'Sam Chen', username to 'schen', email to 'sam.chen@acmecorp.io'.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    user = state.get("currentUser", {})

    checks = [
        (user.get("fullName") == "Sam Chen", f"fullName is '{user.get('fullName')}', expected 'Sam Chen'"),
        (user.get("username") == "schen", f"username is '{user.get('username')}', expected 'schen'"),
        (user.get("email") == "sam.chen@acmecorp.io", f"email is '{user.get('email')}', expected 'sam.chen@acmecorp.io'"),
    ]
    for passed, msg in checks:
        if not passed:
            return False, msg
    return True, "User profile updated correctly."
