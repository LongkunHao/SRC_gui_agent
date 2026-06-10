import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    has_job_12 = "job_12" in saved_job_ids
    has_job_29 = "job_29" in saved_job_ids

    if not has_job_12 and not has_job_29:
        return False, (
            f"Neither Anthropic job is saved. "
            f"job_12 (Research Engineer Intern) and job_29 (Policy Research Intern) are both missing. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if not has_job_12:
        return False, (
            f"job_12 (Research Engineer Intern, Anthropic) is not in savedJobIds. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if not has_job_29:
        return False, (
            f"job_29 (Policy Research Intern, Anthropic) is not in savedJobIds. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        f"Both Anthropic jobs saved: job_12 and job_29. "
        f"Current savedJobIds: {saved_job_ids}"
    )
