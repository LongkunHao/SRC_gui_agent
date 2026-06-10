import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check that job_24 (Amazon PM Intern) is NOT in currentUser.savedJobIds
    current_user = state.get("currentUser", {})
    saved_job_ids = current_user.get("savedJobIds", [])

    if "job_24" in saved_job_ids:
        return False, f"job_24 (Amazon PM Intern) is still in savedJobIds: {saved_job_ids}"

    return True, "Successfully removed Amazon PM Intern (job_24) from saved jobs."
