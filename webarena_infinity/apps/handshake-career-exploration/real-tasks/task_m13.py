import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    job_functions = state.get("currentUser", {}).get("careerInterests", {}).get("jobFunctions", [])

    has_data_analytics = "Data Analytics" in job_functions
    has_research = "Research" in job_functions

    if has_data_analytics:
        return False, (
            f"'Data Analytics' is still in jobFunctions. "
            f"Current jobFunctions: {job_functions}"
        )

    if not has_research:
        return False, (
            f"'Research' is not in jobFunctions. "
            f"Current jobFunctions: {job_functions}"
        )

    return True, (
        f"'Data Analytics' removed and 'Research' added successfully. "
        f"Current jobFunctions: {job_functions}"
    )
