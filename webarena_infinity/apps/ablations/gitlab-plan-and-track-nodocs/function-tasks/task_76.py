import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [i for i in state["iterations"] if i["title"] == "Design Cycle 6"]
    if not match:
        return False, "Iteration 'Design Cycle 6' not found."
    iteration = match[0]
    if iteration["cadenceId"] != 2:
        return False, f"Cadence is {iteration['cadenceId']}, expected 2 (Design Cycles)."
    if iteration["startDate"] != "2026-04-21":
        return False, f"Start date is '{iteration['startDate']}', expected '2026-04-21'."
    if iteration["endDate"] != "2026-05-11":
        return False, f"End date is '{iteration['endDate']}', expected '2026-05-11'."
    return True, "Iteration 'Design Cycle 6' created in Design Cycles cadence."
