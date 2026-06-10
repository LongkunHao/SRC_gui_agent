import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Marcus Johnson (pat_003)
    patients = state.get("patients", [])
    johnson = None
    for p in patients:
        if p.get("lastName") == "Johnson":
            johnson = p
            break
    if not johnson:
        return False, "Patient with lastName 'Johnson' not found."

    patient_id = johnson.get("id", "pat_003")

    # Find all problems for Johnson
    problems = state.get("problems", [])
    johnson_problems = [pr for pr in problems if pr.get("patientId") == patient_id]
    if not johnson_problems:
        return False, "No problems found for Marcus Johnson."

    # The 4 originally active problems: prob_011, prob_012, prob_013, prob_014
    target_ids = {"prob_011", "prob_012", "prob_013", "prob_014"}

    # Check that none of Johnson's problems have status "Active"
    still_active = []
    for pr in johnson_problems:
        if pr.get("status") == "Active":
            still_active.append(f"{pr.get('id', '?')} ({pr.get('title', '?')})")

    if still_active:
        return False, f"The following problems for Johnson are still Active: {', '.join(still_active)}"

    # Verify the 4 target problems exist and are not Active
    found_targets = {pr.get("id") for pr in johnson_problems} & target_ids
    if len(found_targets) < len(target_ids):
        missing = target_ids - found_targets
        return False, f"Expected problems not found for Johnson: {missing}"

    return True, "All of Marcus Johnson's active problems have been marked as controlled (none remain Active)."
