import requests


def verify(server_url: str) -> tuple[bool, str]:
    """PA number year-based: 2025 PA renewed, 2026 PA on hold."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # rx_014 (Apixaban, PA-2025-88432) -> renewed with 5 refills
    rx_014 = next((r for r in state["prescriptions"] if r["id"] == "rx_014"), None)
    if not rx_014:
        errors.append("Prescription rx_014 (Apixaban) not found.")
    elif rx_014.get("refillsRemaining", 0) < 5:
        errors.append(f"Expected rx_014 (Apixaban, PA-2025) refillsRemaining >= 5, got {rx_014.get('refillsRemaining')}.")

    # rx_030 (Semaglutide, PA-2026-10234) -> on-hold
    rx_030 = next((r for r in state["prescriptions"] if r["id"] == "rx_030"), None)
    if not rx_030:
        errors.append("Prescription rx_030 (Semaglutide) not found.")
    elif rx_030.get("status") != "on-hold":
        errors.append(f"Expected rx_030 (Semaglutide, PA-2026) status 'on-hold', got '{rx_030.get('status')}'.")

    if errors:
        return False, " ".join(errors)
    return True, "PA prescriptions handled correctly: 2025 PA renewed, 2026 PA on hold."
