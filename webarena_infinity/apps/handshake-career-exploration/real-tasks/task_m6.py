import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    career_community = (
        state.get("currentUser", {})
        .get("careerInterests", {})
        .get("careerCommunity", "")
    )

    if career_community == "Science & Research":
        return True, f"Career community successfully changed to '{career_community}'."
    return False, (
        f"Career community is '{career_community}', expected 'Science & Research'."
    )
