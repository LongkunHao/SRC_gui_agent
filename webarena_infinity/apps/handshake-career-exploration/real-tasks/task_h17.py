import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Dynamically find all jobs with 'AI/ML' in their labels
    jobs = state.get("jobs", [])
    ai_ml_employer_ids = set()
    for job in jobs:
        labels = job.get("labels", [])
        if "AI/ML" in labels:
            employer_id = job.get("employerId", "")
            if employer_id:
                ai_ml_employer_ids.add(employer_id)

    if not ai_ml_employer_ids:
        return False, "No jobs with 'AI/ML' label found in state."

    followed = state.get("currentUser", {}).get("followedEmployerIds", [])
    followed_set = set(followed)

    missing = ai_ml_employer_ids - followed_set
    if missing:
        # Map employer IDs to names for better diagnostics
        employers = state.get("employers", [])
        emp_names = {e.get("id"): e.get("name") for e in employers}
        missing_details = [f"{eid} ({emp_names.get(eid, 'unknown')})" for eid in missing]
        return False, (
            f"Not all employers with AI/ML jobs are followed. "
            f"Missing: {missing_details}. Currently following: {followed}"
        )

    # Map for success message
    employers = state.get("employers", [])
    emp_names = {e.get("id"): e.get("name") for e in employers}
    followed_details = [f"{eid} ({emp_names.get(eid, 'unknown')})" for eid in ai_ml_employer_ids]

    return True, (
        f"All employers with AI/ML jobs are followed: {followed_details}."
    )
