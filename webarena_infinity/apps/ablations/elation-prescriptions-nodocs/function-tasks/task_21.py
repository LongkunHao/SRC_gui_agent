import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    prescriptions = state.get("prescriptions", [])

    rx = next((p for p in prescriptions if p["id"] == "rx_003"), None)
    if not rx:
        return False, "Prescription rx_003 (Metformin) not found."

    sig = rx.get("sig") or ""
    if "once daily with dinner" not in sig.lower():
        return False, f"Prescription rx_003 sig is '{sig}', expected it to contain 'once daily with dinner'."

    return True, "Prescription rx_003 (Metformin) sig contains 'once daily with dinner'."
