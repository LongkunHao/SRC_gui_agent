import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prescriptions = state.get("prescriptions", [])

    rx = next((p for p in prescriptions if p.get("id") == "rx_005"), None)
    if rx is None:
        return False, "Prescription rx_005 not found in state."

    if rx.get("status") != "active":
        return False, f"rx_005 status should be 'active', got '{rx.get('status')}'."

    if rx.get("refillsRemaining") != 3:
        return False, f"rx_005 refillsRemaining should be 3, got {rx.get('refillsRemaining')}."

    if rx.get("refillsTotal") != 3:
        return False, f"rx_005 refillsTotal should be 3, got {rx.get('refillsTotal')}."

    history = rx.get("history", [])
    renewed = any(h.get("action") == "renewed" for h in history)
    if not renewed:
        return False, "rx_005 history does not contain a 'renewed' entry."

    return True, "rx_005 (Pantoprazole) renewed with 3 refills."
