import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    roles = state.get("currentUser", {}).get("careerInterests", {}).get("roles", [])

    if "Machine Learning Engineer" in roles:
        return True, f"'Machine Learning Engineer' found in preferred roles: {roles}"
    return False, f"'Machine Learning Engineer' not found in preferred roles. Current roles: {roles}"
