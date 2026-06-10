import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    job_types = state.get("currentUser", {}).get("careerInterests", {}).get("jobTypes", [])

    if "On-campus" in job_types:
        return True, f"'On-campus' found in jobTypes: {job_types}"

    return False, (
        f"'On-campus' not found in jobTypes. "
        f"Current jobTypes: {job_types}"
    )
