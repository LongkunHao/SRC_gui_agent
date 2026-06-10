import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    career = state.get("currentUser", {}).get("careerInterests", {})
    roles = career.get("roles", [])
    job_types = career.get("jobTypes", [])
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    errors = []

    if "Product Manager" not in roles:
        errors.append(f"'Product Manager' not in roles. Current roles: {roles}")

    if "Full-time" not in job_types:
        errors.append(f"'Full-time' not in jobTypes. Current jobTypes: {job_types}")

    if "job_18" not in saved_job_ids:
        errors.append(f"job_18 (Nike PM Intern) not in savedJobIds. Current savedJobIds: {saved_job_ids}")

    if "job_24" not in saved_job_ids:
        errors.append(f"job_24 (Amazon PM Intern) not in savedJobIds. Current savedJobIds: {saved_job_ids}")

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"All checks passed: 'Product Manager' in roles, 'Full-time' in jobTypes, "
        f"job_18 and job_24 in savedJobIds."
    )
