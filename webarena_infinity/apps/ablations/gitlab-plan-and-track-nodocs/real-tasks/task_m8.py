import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    iteration = next((it for it in state["iterations"] if it["title"] == "Design Cycle 6"), None)
    if iteration is None:
        return False, "Iteration with title 'Design Cycle 6' not found."

    if iteration.get("cadenceId") != 2:
        return False, f"cadenceId is {iteration.get('cadenceId')}, expected 2."

    if iteration.get("startDate") != "2026-06-15":
        return False, f"startDate is '{iteration.get('startDate')}', expected '2026-06-15'."

    if iteration.get("endDate") != "2026-07-05":
        return False, f"endDate is '{iteration.get('endDate')}', expected '2026-07-05'."

    return True, "Iteration 'Design Cycle 6' created with correct cadence and dates."
