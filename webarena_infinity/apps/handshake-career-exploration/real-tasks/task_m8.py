import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    industries = (
        state.get("currentUser", {})
        .get("careerInterests", {})
        .get("industries", [])
    )

    has_finance = "Finance" in industries
    has_consulting = "Consulting" in industries

    if has_finance:
        return False, (
            f"'Finance' is still in preferred industries. Current industries: {industries}"
        )
    if not has_consulting:
        return False, (
            f"'Consulting' not found in preferred industries. Current industries: {industries}"
        )

    return True, (
        f"'Finance' removed and 'Consulting' added successfully. Current industries: {industries}"
    )
