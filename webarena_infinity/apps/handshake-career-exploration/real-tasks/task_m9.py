import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    linkedin_url = state.get("currentUser", {}).get("linkedinUrl", "")

    if linkedin_url == "linkedin.com/in/maya-chen-cs":
        return True, f"LinkedIn URL successfully updated to '{linkedin_url}'."
    return False, (
        f"LinkedIn URL is '{linkedin_url}', expected 'linkedin.com/in/maya-chen-cs'."
    )
