import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prescriptions = state.get("prescriptions", [])

    rx = next((p for p in prescriptions if p.get("id") == "rx_007"), None)
    if rx is None:
        return False, "Prescription rx_007 not found in state."

    if rx.get("quantity") != 180:
        return False, f"rx_007 quantity should be 180, got {rx.get('quantity')}."

    history = rx.get("history", [])
    modified = any(h.get("action") == "modified" for h in history)
    if not modified:
        return False, "rx_007 history does not contain a 'modified' entry."

    return True, "rx_007 (Gabapentin) quantity changed to 180."
