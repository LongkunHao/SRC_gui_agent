import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    # Active internships in San Francisco
    required_jobs = {
        "job_02": "Google APM Intern",
        "job_09": "Stripe Backend Eng Intern",
        "job_12": "Anthropic Research Eng Intern",
        "job_29": "Anthropic Policy Research Intern",
        "job_30": "Salesforce Marketing Analyst Intern",
    }

    missing = []
    for job_id, job_name in required_jobs.items():
        if job_id not in saved_job_ids:
            missing.append(f"{job_id} ({job_name})")

    if missing:
        return False, (
            f"Not all active SF internships are saved. "
            f"Missing: {missing}. Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        f"All active SF internships saved: {list(required_jobs.keys())}. "
        f"Current savedJobIds: {saved_job_ids}"
    )
