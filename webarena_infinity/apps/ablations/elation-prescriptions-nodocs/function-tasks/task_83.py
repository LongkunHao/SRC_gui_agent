import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prescriptions = state.get("prescriptions", [])

    rx = next((p for p in prescriptions if p.get("id") == "rx_002"), None)
    if rx is None:
        return False, "Prescription rx_002 not found in state."

    if rx.get("dosage") != "10mg":
        return False, f"rx_002 dosage should be '10mg', got '{rx.get('dosage')}'."

    history = rx.get("history", [])
    modified = any(h.get("action") == "modified" for h in history)
    if not modified:
        return False, "rx_002 history does not contain a 'modified' entry."

    return True, "rx_002 (Amlodipine) dosage changed to 10mg."
