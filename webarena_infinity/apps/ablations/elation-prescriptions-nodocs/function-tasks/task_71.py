import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prescriptions = state.get("prescriptions", [])

    rx = next((p for p in prescriptions if p.get("id") == "rx_030"), None)
    if rx is None:
        return False, "Prescription rx_030 not found in state."

    sig = rx.get("sig", "")
    if "same day each week" not in sig.lower():
        return False, f"rx_030 sig should contain 'same day each week', got '{sig}'."

    history = rx.get("history", [])
    modified = any(h.get("action") == "modified" for h in history)
    if not modified:
        return False, "rx_030 history does not contain a 'modified' entry."

    return True, "rx_030 (Semaglutide) sig updated to contain 'same day each week'."
