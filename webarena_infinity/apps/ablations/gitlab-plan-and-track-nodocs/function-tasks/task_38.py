import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    iteration = next((i for i in state["iterations"] if i["title"] == "Sprint 9"), None)
    if not iteration:
        return False, "Iteration 'Sprint 9' not found."

    # Engineering Sprints cadence = id 1
    if iteration["cadenceId"] != 1:
        return False, f"Cadence id is {iteration['cadenceId']}, expected 1 (Engineering Sprints)."

    if iteration["startDate"] != "2026-04-28":
        return False, f"Start date is '{iteration['startDate']}', expected '2026-04-28'."

    if iteration["endDate"] != "2026-05-11":
        return False, f"End date is '{iteration['endDate']}', expected '2026-05-11'."

    return True, "Iteration 'Sprint 9' created in Engineering Sprints cadence."
